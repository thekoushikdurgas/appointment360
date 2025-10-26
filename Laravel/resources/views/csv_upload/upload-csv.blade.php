<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload CSV to S3 via Chunked Upload</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
        h2 { color: #333; }
        .upload-container { 
            background: #f9f9f9; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .file-input-wrapper {
            margin: 20px 0;
        }
        input[type="file"] {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 4px;
            width: 100%;
            max-width: 400px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background: #45a049;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .progress-container {
            margin-top: 20px;
            display: none;
        }
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        #progressText {
            color: #555;
            font-size: 14px;
        }
        #message { 
            margin-top: 15px; 
            padding: 15px;
            border-radius: 4px;
            font-weight: bold;
            display: none;
        }
        .success-msg {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error-msg {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .file-info {
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="upload-container">
        <h2>Upload CSV File to S3</h2>
        <p style="color: #666;">Supports large CSV files up to 500MB using chunked upload technology.</p>

        <form id="csvUploadForm" enctype="multipart/form-data">
            <div class="file-input-wrapper">
                <input type="file" name="csv_file" accept=".csv" required id="fileInput">
                <div class="file-info" id="fileInfo"></div>
            </div>
            <button type="submit" id="uploadBtn">Upload & Import</button>
            <button type="button" id="cancelBtn" style="background: #f44336; display: none;">Cancel Upload</button>
        </form>

        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill">0%</div>
            </div>
            <div id="progressText">Preparing upload...</div>
        </div>
        
        <div id="message"></div>
    </div>

    <script>
        const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB chunks
        let currentUploadId = null;
        let isUploading = false;

        // Display file info when selected
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                document.getElementById('fileInfo').textContent = 
                    `Selected: ${file.name} (${sizeMB} MB)`;
            }
        });

        // Handle form submission
        document.getElementById('csvUploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('fileInput');
            if (!fileInput.files.length) {
                showMessage('Please select a CSV file.', 'error');
                return;
            }

            const file = fileInput.files[0];
            
            // Validate file type
            if (!file.name.toLowerCase().endsWith('.csv')) {
                showMessage('Please select a valid CSV file.', 'error');
                return;
            }

            // Start chunked upload
            await startChunkedUpload(file);
        });

        // Cancel upload
        document.getElementById('cancelBtn').addEventListener('click', async function() {
            if (currentUploadId && isUploading) {
                if (confirm('Are you sure you want to cancel this upload?')) {
                    await cancelUpload();
                }
            }
        });

        async function startChunkedUpload(file) {
            isUploading = true;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            // Disable upload button
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('cancelBtn').style.display = 'inline-block';
            document.getElementById('message').style.display = 'none';
            
            // Show progress
            document.getElementById('progressContainer').style.display = 'block';
            updateProgress(0, 'Initializing upload...');

            try {
                const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

                // Step 1: Initialize upload
                updateProgress(0, `Preparing to upload ${totalChunks} chunks...`);
                const initResponse = await fetch("{{ route('csv.upload.init') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': csrfToken,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        fileName: file.name,
                        fileSize: file.size,
                        totalChunks: totalChunks
                    })
                });

                const initData = await initResponse.json();
                if (!initData.success) {
                    throw new Error(initData.message || 'Failed to initialize upload');
                }

                currentUploadId = initData.uploadId;

                // Step 2: Upload chunks
                for (let i = 0; i < totalChunks; i++) {
                    if (!isUploading) {
                        throw new Error('Upload cancelled');
                    }

                    const start = i * CHUNK_SIZE;
                    const end = Math.min(start + CHUNK_SIZE, file.size);
                    const chunk = file.slice(start, end);

                    const chunkFormData = new FormData();
                    chunkFormData.append('uploadId', currentUploadId);
                    chunkFormData.append('chunkIndex', i);
                    chunkFormData.append('chunk', chunk);

                    updateProgress(
                        ((i + 1) / totalChunks) * 90, 
                        `Uploading chunk ${i + 1} of ${totalChunks}...`
                    );

                    const chunkResponse = await fetch("{{ route('csv.upload.chunk') }}", {
                        method: 'POST',
                        headers: {
                            'X-CSRF-TOKEN': csrfToken,
                            'Accept': 'application/json'
                        },
                        body: chunkFormData
                    });

                    const chunkData = await chunkResponse.json();
                    if (!chunkData.success) {
                        throw new Error(chunkData.message || `Failed to upload chunk ${i + 1}`);
                    }
                }

                // Step 3: Complete upload
                updateProgress(95, 'Finalizing upload...');
                const completeResponse = await fetch("{{ route('csv.upload.complete') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': csrfToken,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        uploadId: currentUploadId
                    })
                });

                const completeData = await completeResponse.json();
                if (!completeData.success) {
                    throw new Error(completeData.message || 'Failed to complete upload');
                }

                updateProgress(100, 'Upload complete!');
                showMessage(completeData.message, 'success');
                
                // Reset form
                setTimeout(() => {
                    document.getElementById('csvUploadForm').reset();
                    document.getElementById('fileInfo').textContent = '';
                    document.getElementById('progressContainer').style.display = 'none';
                }, 3000);

            } catch (error) {
                console.error('Upload error:', error);
                showMessage('Upload failed: ' + error.message, 'error');
                
                // Try to cancel the upload on S3
                if (currentUploadId) {
                    await cancelUpload(false);
                }
            } finally {
                isUploading = false;
                currentUploadId = null;
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('cancelBtn').style.display = 'none';
            }
        }

        async function cancelUpload(showMsg = true) {
            isUploading = false;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            try {
                await fetch("{{ route('csv.upload.cancel') }}", {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': csrfToken,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        uploadId: currentUploadId
                    })
                });

                if (showMsg) {
                    showMessage('Upload cancelled.', 'error');
                }
            } catch (error) {
                console.error('Cancel error:', error);
            }

            currentUploadId = null;
            document.getElementById('uploadBtn').disabled = false;
            document.getElementById('cancelBtn').style.display = 'none';
            document.getElementById('progressContainer').style.display = 'none';
        }

        function updateProgress(percent, text) {
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            progressFill.style.width = percent + '%';
            progressFill.textContent = Math.round(percent) + '%';
            progressText.textContent = text;
        }

        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = text;
            messageDiv.className = type === 'success' ? 'success-msg' : 'error-msg';
            messageDiv.style.display = 'block';
        }
    </script>
</body>
</html>