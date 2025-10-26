<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="csrf-token" content="{{ csrf_token() }}">
  <title>CSV Upload to S3</title>
  <style>
    #progressBar {
      width: 100%;
      background-color: #f3f3f3;
      margin-top: 10px;
    }
    #progressBar div {
      width: 0%;
      height: 20px;
      background-color: #4caf50;
      text-align: center;
      color: white;
    }
  </style>
</head>
<body>
<h2>Upload CSV to S3</h2>
<input type="file" id="fileInput">
<button id="uploadBtn">Upload</button>
<div id="progressBar"><div></div></div>
<div id="status"></div>

<script>
const CHUNK_SIZE = 5 * 1024 * 1024; // 5 MB per chunk
const MAX_RETRIES = 3;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const progressBar = document.getElementById('progressBar').firstElementChild;
const statusDiv = document.getElementById('status');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Upload button click
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return alert('Please select a file');

    if (file.size <= CHUNK_SIZE) {
        // Small file → direct pre-signed PUT
        await uploadSingle(file);
    } else {
        // Large file → multipart pre-signed upload
        await uploadMultipart(file);
    }
});

// --------------------
// Small file upload
// --------------------
async function uploadSingle(file) {
    statusDiv.textContent = 'Getting pre-signed URL...';

    const presignRes = await fetch("{{ route('upload.getPresignedUploadUrl') }}", {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({fileName: file.name, fileType: file.type})
    });
    const data = await presignRes.json();

    const xhr = new XMLHttpRequest();
    xhr.open('PUT', data.url, true);
    xhr.setRequestHeader('Content-Type', file.type);

    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percent + '%';
            progressBar.textContent = percent + '%';
        }
    };

    xhr.onload = async () => {
        if (xhr.status === 200) {
            progressBar.style.width = '100%';
            progressBar.textContent = '100%';
            statusDiv.textContent = 'Upload complete! Processing CSV...';

            // Trigger Laravel job
            await fetch("{{ route('upload.processCSV') }}", {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({s3Key: data.s3Key})
            });
            statusDiv.textContent = 'CSV job queued!';
        } else {
            statusDiv.textContent = 'Upload failed.';
        }
    };

    xhr.onerror = () => statusDiv.textContent = 'Network error.';
    xhr.send(file);
}

// --------------------
// Large file multipart upload
// --------------------
async function uploadMultipart(file) {
    statusDiv.textContent = 'Getting pre-signed URLs...';

    // Step 1: Get pre-signed URLs for each chunk from Laravel
    const initRes = await fetch("{{ route('upload.getMultipartPresignedUrls') }}", {
        method: 'POST',
        headers: {'X-CSRF-TOKEN': csrfToken,'Content-Type':'application/json'},
        body: JSON.stringify({fileName: file.name, fileSize: file.size, chunkSize: CHUNK_SIZE})
    });
    const initData = await initRes.json();
    const { urls, uploadId, s3Key } = initData;

    const parts = [];

    // Step 2: Upload chunks sequentially
    for (let i = 0; i < urls.length; i++) {
        let retries = 0;
        let success = false;

        while(!success && retries < MAX_RETRIES){
            try {
                const start = i * CHUNK_SIZE;
                const end = Math.min(start + CHUNK_SIZE, file.size);
                const chunk = file.slice(start, end);

                const res = await fetch(urls[i], {
                    method: 'PUT',
                    body: chunk,
                    headers: {'Content-Type': 'application/octet-stream'}
                });

                if(!res.ok) throw new Error('Chunk upload failed');

                const etag = res.headers.get('ETag');
                parts.push({ETag: etag, PartNumber: i+1});

                const percent = Math.round(((i + 1) / urls.length) * 100);
                progressBar.style.width = percent + '%';
                progressBar.textContent = percent + '%';

                success = true;
            } catch(e){
                retries++;
                if(retries === MAX_RETRIES){
                    statusDiv.textContent = `Chunk ${i} failed after ${MAX_RETRIES} retries.`;
                    return;
                }
            }
        }
    }

    // Step 3: Complete multipart upload
    const completeRes = await fetch("{{ route('upload.completeMultipartUpload') }}", {
        method:'POST',
        headers:{'X-CSRF-TOKEN': csrfToken,'Content-Type':'application/json'},
        body: JSON.stringify({s3Key, uploadId, parts})
    });
    const completeJson = await completeRes.json();
    if(completeJson.success) statusDiv.textContent = '✅ Upload complete and CSV job queued!';
    else statusDiv.textContent = '❌ Upload failed: '+completeJson.message;
}
</script>
</body>
</html>
