"""
Import views for CSV import functionality
Enhanced with local file selection and improved preview
"""
import json
import os
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from pathlib import Path
import pandas as pd

from apps.imports.models import ImportJob
from services.csv_column_mapper import CSVColumnMapper
from services.file_validator import FileValidator
from apps.imports.tasks import process_import_task
import json
import ast


@login_required
def upload_view(request):
    """CSV upload and preview with local file selection support"""
    # Check for local file selection or upload
    selected_file_path = None
    filename = None
    
    if request.method == 'POST':
        # Handle file upload
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            
            # Save file temporarily
            file_path = default_storage.save(f'temp/{uploaded_file.name}', uploaded_file)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            selected_file_path = full_path
            filename = uploaded_file.name
        
        # Handle local file path
        elif request.POST.get('local_file_path'):
            file_path = request.POST.get('local_file_path')
            
            # Validate file path
            is_valid, error_msg = FileValidator.validate_local_path(file_path)
            
            if not is_valid:
                messages.error(request, f"Invalid file: {error_msg}")
                return render(request, 'imports/upload.html', {
                    'csv_files': FileValidator.list_csv_files(settings.BASE_DIR / 'data')
                })
            
            selected_file_path = file_path
            filename = os.path.basename(file_path)
    
    # If a file has been selected, show preview
    if selected_file_path and filename:
        try:
            # Get file size
            file_size_mb = FileValidator.get_file_size_mb(selected_file_path)
            
            # Read CSV for preview (first 10 rows)
            df = pd.read_csv(selected_file_path, nrows=10)
            total_rows = len(pd.read_csv(selected_file_path))  # Get total rows for preview
            
            # Auto-detect column mapping
            mapper = CSVColumnMapper()
            auto_mapping = mapper.auto_map_columns(df)
            mapping_json = json.dumps(auto_mapping)
            
            context = {
                'filename': filename,
                'file_path': selected_file_path,
                'file_size_mb': file_size_mb,
                'total_rows': total_rows,
                'preview': df.to_html(classes='table table-striped', index=False),
                'preview_rows': df.head(10).to_dict('records'),
                'columns': df.columns.tolist(),
                'auto_mapping': auto_mapping,
                'mapping_json': mapping_json,
                'mapping_count': len(auto_mapping),
            }
            
            return render(request, 'imports/preview.html', context)
            
        except Exception as e:
            messages.error(request, f"Error reading file: {str(e)}")
    
    # List local CSV files for selection
    csv_files = FileValidator.list_csv_files(settings.BASE_DIR / 'data')
    
    return render(request, 'imports/upload.html', {
        'csv_files': csv_files
    })


@login_required
def start_import_view(request):
    """Start import job"""
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        mapping_json = request.POST.get('mapping')
        
        if file_path and mapping_json:
            # Ensure mapping_json is valid JSON
            try:
                mapping = json.loads(mapping_json)
            except json.JSONDecodeError:
                try:
                    # Fallback if the value came in as a python-dict-like string
                    mapping = ast.literal_eval(mapping_json)
                except Exception:
                    messages.error(request, 'Invalid column mapping format')
                    return redirect('imports:upload')
            
            # Create import job
            job = ImportJob.objects.create(
                user_id=str(request.user.id),
                filename=os.path.basename(file_path),
                file_size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                status='PENDING',
                column_mapping=json.dumps(mapping)
            )
            
            # Trigger background task
            process_import_task.delay(job.id, file_path, mapping, str(request.user.id))
            
            messages.success(request, f'Import job #{job.id} started!')
            return redirect('imports:progress', job_id=job.id)
    
    messages.error(request, 'Invalid import parameters')
    return redirect('imports:upload')


@login_required
def progress_view(request, job_id):
    """View import progress"""
    job = ImportJob.objects.get(id=job_id)
    
    context = {
        'job': job,
        'progress': job.get_progress_percentage(),
    }
    
    return render(request, 'imports/progress.html', context)


@login_required
def job_status_api(request, job_id):
    """Return job status as JSON for AJAX polling"""
    try:
        job = get_object_or_404(ImportJob, id=job_id)
        
        # Calculate additional metrics
        processing_speed = 0
        estimated_completion = None
        duration = None
        
        if job.started_at:
            if job.completed_at:
                # Calculate total duration
                duration = str(job.completed_at - job.started_at)
            elif job.status == 'PROCESSING' and job.processed_rows > 0:
                # Calculate processing speed
                elapsed = timezone.now() - job.started_at
                if elapsed.total_seconds() > 0:
                    processing_speed = job.processed_rows / elapsed.total_seconds()
                    
                    # Estimate completion time
                    if processing_speed > 0 and job.total_rows > job.processed_rows:
                        remaining_rows = job.total_rows - job.processed_rows
                        eta_seconds = remaining_rows / processing_speed
                        estimated_completion = timezone.now() + timedelta(seconds=eta_seconds)
        
        data = {
            'id': job.id,
            'status': job.status,
            'progress_percentage': job.get_progress_percentage(),
            'total_rows': job.total_rows,
            'processed_rows': job.processed_rows,
            'success_count': job.success_count,
            'error_count': job.error_count,
            'duplicate_count': job.duplicate_count,
            'processing_speed': processing_speed,
            'current_batch': job.current_batch,
            'total_batches': job.total_batches,
            'estimated_completion': estimated_completion.isoformat() if estimated_completion else None,
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'duration': duration,
            'error_log': job.error_log,
            'last_updated': timezone.now().isoformat(),
            'is_complete': job.is_complete(),
            'is_running': job.is_running()
        }
        
        return JsonResponse(data)
        
    except ImportJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def cancel_job_api(request, job_id):
    """Cancel a running import job"""
    try:
        job = get_object_or_404(ImportJob, id=job_id)
        
        if job.is_complete():
            return JsonResponse({'error': 'Job is already complete'}, status=400)
        
        # Update job status
        job.status = 'CANCELLED'
        job.completed_at = timezone.now()
        job.save()
        
        # TODO: Send cancellation signal to Celery task
        
        return JsonResponse({
            'success': True,
            'message': 'Job cancelled successfully',
            'status': job.status
        })
        
    except ImportJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def recent_jobs_api(request):
    """Get recent jobs for user"""
    try:
        # Get user's recent jobs (last 10)
        jobs = ImportJob.objects.filter(
            user_id=str(request.user.id)
        ).order_by('-created_at')[:10]
        
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'filename': job.filename,
                'status': job.status,
                'progress_percentage': job.get_progress_percentage(),
                'created_at': job.created_at.strftime('%Y-%m-%d %H:%M'),
                'success_count': job.success_count,
                'error_count': job.error_count,
                'duplicate_count': job.duplicate_count
            })
        
        return JsonResponse({
            'jobs': jobs_data,
            'total': len(jobs_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

