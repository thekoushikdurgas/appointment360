@extends('admin.layouts.app')

@section('title')
{{'Import Contact'}}
@endsection

@section('content')
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">  Import Contact</h1>

    </div>
    @include('component.error-message')                    

    <div class="row">                        

        <div                             class="col-lg-12">

            <form id="csv-import-form" enctype="multipart/form-data">
                
                @csrf
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                    </div>
                    <div class="card-body">
                        <div class="row">
                            
                            <div class="  form-group">
                                <label>
                                Upload CSV File
                            </label>
  <input type="file" name="csv_file" required>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button type="submit" class="btn btn-primary" name="upload">Import</button>
                        <a href="{{ route('admin.contacts')}}" class="btn btn-danger">Cancel</a>
                    </div>
					
					<div id="progress-container" style="margin-top:20px; display:none;">
    <div id="progress-bar" style="width:0%; height:25px; background:green; color:white; text-align:center;">0%</div>
</div>

<div id="status"></div>
                </div>

            </form>
        </div>
    </div>
</div>

@endsection
@section('js-footer')

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$('#csv-import-form').on('submit', function(e) {
    e.preventDefault();

    var formData = new FormData(this);

    $('#progress-container').show();
    $('#progress-bar').css('width', '0%').text('0%');

    $.ajax({
        url: "{{ route('contacts.import') }}",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#status').html('<p>' + response.message + '</p>');

            var interval = setInterval(function() {
                $.get("{{ route('contacts.import.progress') }}", function(progressResponse) {
                    var total = progressResponse.total || 1;
                    var percent = Math.min((progressResponse.progress / total) * 100, 100);
                    $('#progress-bar').css('width', percent + '%').text(Math.floor(percent) + '%');
                    if(percent >= 100) clearInterval(interval);
                });
            }, 2000);
        },
        error: function(xhr) {
            $('#status').html('<p style="color:red">Error: ' + xhr.responseText + '</p>');
        }
    });
});
</script>
@endsection