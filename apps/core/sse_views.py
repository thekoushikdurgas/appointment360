"""
Server-Sent Events (SSE) views for real-time updates
"""
import json
import time
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.cache import cache
from apps.imports.models import ImportJob
from apps.exports.models import ExportLog
from apps.contacts.models import Contact


@login_required
@never_cache
@require_http_methods(["GET"])
def sse_updates(request):
    """Server-Sent Events endpoint for real-time updates"""
    
    def event_stream():
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected', 'timestamp': timezone.now().isoformat()})}\n\n"
        
        last_import_update = None
        last_export_update = None
        last_contact_update = None
        
        while True:
            try:
                # Check for import job updates
                latest_import = ImportJob.objects.filter(
                    user=request.user
                ).order_by('-updated_at').first()
                
                if latest_import and (not last_import_update or latest_import.updated_at > last_import_update):
                    yield f"data: {json.dumps({
                        'type': 'import_update',
                        'data': {
                            'id': latest_import.id,
                            'status': latest_import.status,
                            'progress_percentage': latest_import.progress_percentage,
                            'total_rows': latest_import.total_rows,
                            'processed_rows': latest_import.processed_rows,
                            'success_count': latest_import.success_count,
                            'error_count': latest_import.error_count,
                            'duplicate_count': latest_import.duplicate_count,
                            'processing_speed': latest_import.processing_speed,
                            'current_batch': latest_import.current_batch,
                            'total_batches': latest_import.total_batches,
                            'estimated_completion': latest_import.estimated_completion.isoformat() if latest_import.estimated_completion else None,
                            'started_at': latest_import.started_at.isoformat() if latest_import.started_at else None,
                            'completed_at': latest_import.completed_at.isoformat() if latest_import.completed_at else None,
                            'error_log': latest_import.error_log,
                            'is_complete': latest_import.is_complete,
                            'is_running': latest_import.is_running
                        },
                        'timestamp': timezone.now().isoformat()
                    })}\n\n"
                    last_import_update = latest_import.updated_at
                
                # Check for export updates
                latest_export = ExportLog.objects.filter(
                    user=request.user
                ).order_by('-updated_at').first()
                
                if latest_export and (not last_export_update or latest_export.updated_at > last_export_update):
                    yield f"data: {json.dumps({
                        'type': 'export_update',
                        'data': {
                            'id': latest_export.id,
                            'export_type': latest_export.export_type,
                            'export_format': latest_export.export_format,
                            'status': latest_export.status,
                            'progress_percentage': latest_export.progress_percentage,
                            'record_count': latest_export.record_count,
                            'file_size': latest_export.file_size,
                            'filename': latest_export.filename,
                            'created_at': latest_export.created_at.isoformat(),
                            'started_at': latest_export.started_at.isoformat() if latest_export.started_at else None,
                            'completed_at': latest_export.completed_at.isoformat() if latest_export.completed_at else None,
                            'error_message': latest_export.error_message,
                            'is_completed': latest_export.is_completed,
                            'is_failed': latest_export.is_failed,
                            'is_processing': latest_export.is_processing
                        },
                        'timestamp': timezone.now().isoformat()
                    })}\n\n"
                    last_export_update = latest_export.updated_at
                
                # Check for contact count updates
                current_contact_count = Contact.objects.filter(user=request.user).count()
                cached_contact_count = cache.get(f'contact_count_{request.user.id}', 0)
                
                if current_contact_count != cached_contact_count:
                    cache.set(f'contact_count_{request.user.id}', current_contact_count, 300)
                    yield f"data: {json.dumps({
                        'type': 'contact_count_update',
                        'data': {
                            'count': current_contact_count,
                            'previous_count': cached_contact_count
                        },
                        'timestamp': timezone.now().isoformat()
                    })}\n\n"
                
                # Check for system notifications
                notifications = cache.get(f'notifications_{request.user.id}', [])
                if notifications:
                    for notification in notifications:
                        yield f"data: {json.dumps({
                            'type': 'notification',
                            'data': notification,
                            'timestamp': timezone.now().isoformat()
                        })}\n\n"
                    cache.delete(f'notifications_{request.user.id}')
                
                # Send heartbeat every 30 seconds
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': timezone.now().isoformat()})}\n\n"
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'timestamp': timezone.now().isoformat()})}\n\n"
                time.sleep(5)  # Wait longer on error
    
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Cache-Control'
    
    return response


@login_required
@require_http_methods(["POST"])
def send_notification(request):
    """Send a notification to a user via SSE"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        message = data.get('message')
        notification_type = data.get('type', 'info')
        
        if not user_id or not message:
            return JsonResponse({'error': 'user_id and message are required'}, status=400)
        
        # Store notification in cache
        notifications = cache.get(f'notifications_{user_id}', [])
        notifications.append({
            'message': message,
            'type': notification_type,
            'timestamp': timezone.now().isoformat()
        })
        cache.set(f'notifications_{user_id}', notifications, 300)
        
        return JsonResponse({'success': True, 'message': 'Notification sent'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def sse_status(request):
    """Get SSE connection status"""
    return JsonResponse({
        'status': 'active',
        'timestamp': timezone.now().isoformat(),
        'user_id': request.user.id
    })
