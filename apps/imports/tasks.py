"""
Celery tasks for background import processing
Enhanced with type conversion, error tracking, and bulk operations
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from apps.imports.models import ImportJob
from apps.contacts.models import Contact
from services.contact_service import ContactService, validate_email
from services.type_converter import TypeConverter
from services.bulk_insert_service import BulkInsertService
from services.import_error_tracker import ImportErrorTracker
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@shared_task(bind=True)
def process_import_task(self, job_id, file_path, mapping, user_id):
    """
    Process CSV import in background with enhanced progress tracking
    
    Args:
        job_id: ImportJob ID
        file_path: Path to CSV file
        mapping: Column mapping dictionary
        user_id: User ID
    """
    job = ImportJob.objects.get(id=job_id)
    
    # Initialize services
    bulk_service = BulkInsertService()
    
    try:
        # Update job status and start time
        job.status = 'PROCESSING'
        job.started_at = timezone.now()
        job.save()
        
        # Read CSV file
        df = pd.read_csv(file_path)
        job.total_rows = len(df)
        job.total_batches = (len(df) // 1000) + 1
        job.save()
        
        # Get channel layer for WebSocket updates
        channel_layer = get_channel_layer()
        
        start_time = timezone.now()
        
        # Process in batches
        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            # Use bulk insert service
            batch_results = bulk_service.bulk_insert_from_dataframe(
                batch, str(user_id), mapping
            )
            
            # Update job progress
            job.processed_rows = i + len(batch)
            job.success_count = batch_results['success_count']
            job.error_count = batch_results['error_count']
            job.duplicate_count = batch_results['duplicate_count']
            job.current_batch = (i // batch_size) + 1
            
            # Calculate processing speed
            elapsed = timezone.now() - start_time
            if elapsed.total_seconds() > 0:
                job.processing_speed = job.processed_rows / elapsed.total_seconds()
                
                # Estimate completion time
                if job.processing_speed > 0 and job.total_rows > job.processed_rows:
                    remaining_rows = job.total_rows - job.processed_rows
                    eta_seconds = remaining_rows / job.processing_speed
                    job.estimated_completion = timezone.now() + timedelta(seconds=eta_seconds)
            
            # Store errors in job
            errors_json = bulk_service.get_error_tracker().to_json()
            job.error_log = errors_json
            job.save()
            
            # Send progress update via WebSocket
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f'import_{job_id}',
                    {
                        'type': 'import_progress',
                        'data': {
                            'job_id': job_id,
                            'status': job.status,
                            'processed_rows': job.processed_rows,
                            'total_rows': job.total_rows,
                            'success_count': job.success_count,
                            'error_count': job.error_count,
                            'duplicate_count': job.duplicate_count,
                            'progress': job.get_progress_percentage(),
                            'processing_speed': job.processing_speed,
                            'current_batch': job.current_batch,
                            'total_batches': job.total_batches,
                            'estimated_completion': job.estimated_completion.isoformat() if job.estimated_completion else None,
                            'last_updated': timezone.now().isoformat()
                        }
                    }
                )
            
            # Check if job was cancelled
            job.refresh_from_db()
            if job.status == 'CANCELLED':
                break
        
        # Mark as completed
        job.status = 'COMPLETED'
        job.processed_rows = len(df)
        job.completed_at = timezone.now()
        job.save()
        
        # Send final update
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'import_{job_id}',
                {
                    'type': 'import_progress',
                    'data': {
                        'job_id': job_id,
                        'status': job.status,
                        'processed_rows': job.processed_rows,
                        'total_rows': job.total_rows,
                        'success_count': job.success_count,
                        'error_count': job.error_count,
                        'duplicate_count': job.duplicate_count,
                        'progress': job.get_progress_percentage(),
                        'completed_at': job.completed_at.isoformat(),
                        'duration': str(job.completed_at - job.started_at),
                        'last_updated': timezone.now().isoformat()
                    }
                }
            )
        
        return {
            'success': True,
            'success_count': job.success_count,
            'error_count': job.error_count,
            'duplicate_count': job.duplicate_count
        }
        
    except Exception as e:
        # Mark as failed
        job.status = 'FAILED'
        job.error_log = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        # Send error update
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'import_{job_id}',
                {
                    'type': 'import_progress',
                    'data': {
                        'job_id': job_id,
                        'status': job.status,
                        'error_log': str(e),
                        'completed_at': job.completed_at.isoformat(),
                        'last_updated': timezone.now().isoformat()
                    }
                }
            )
        
        return {
            'success': False,
            'error': str(e)
        }

