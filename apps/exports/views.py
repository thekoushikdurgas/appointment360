"""
Export views with comprehensive history tracking and management
"""
import os
import json
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from .models import ExportLog, ExportLimit
from .tasks import process_export_task


@login_required
def export_history(request):
    """Enhanced export history view with filtering and pagination"""
    # Get filter parameters
    export_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    exports = ExportLog.objects.filter(user=request.user).order_by('-created_at')
    
    # Apply filters
    if export_type:
        exports = exports.filter(export_type=export_type)
    
    if status:
        exports = exports.filter(status=status)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            exports = exports.filter(created_at__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            exports = exports.filter(created_at__date__lte=date_to_obj)
        except ValueError:
            pass
    
    if search:
        exports = exports.filter(
            Q(filename__icontains=search) |
            Q(export_type__icontains=search) |
            Q(export_format__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(exports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_exports': exports.count(),
        'completed_exports': exports.filter(status='completed').count(),
        'failed_exports': exports.filter(status='failed').count(),
        'total_records_exported': exports.filter(status='completed').aggregate(
            total=Sum('record_count')
        )['total'] or 0,
        'total_file_size': exports.filter(status='completed').aggregate(
            total=Sum('file_size')
        )['total'] or 0,
    }
    
    # Export type distribution
    type_distribution = exports.values('export_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Status distribution
    status_distribution = exports.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'page_title': 'Export History',
        'page_obj': page_obj,
        'exports': page_obj,
        'stats': stats,
        'type_distribution': type_distribution,
        'status_distribution': status_distribution,
        'filters': {
            'type': export_type,
            'status': status,
            'date_from': date_from,
            'date_to': date_to,
            'search': search,
        },
        'export_type_choices': ExportLog.EXPORT_TYPE_CHOICES,
        'status_choices': ExportLog.STATUS_CHOICES,
    }
    
    return render(request, 'exports/history.html', context)


@login_required
def export_status_api(request, export_id):
    """API endpoint to get export status"""
    try:
        export = get_object_or_404(ExportLog, id=export_id, user=request.user)
        
        data = {
            'id': export.id,
            'status': export.status,
            'progress_percentage': export.progress_percentage,
            'record_count': export.record_count,
            'file_size': export.file_size,
            'filename': export.filename,
            'created_at': export.created_at.isoformat(),
            'started_at': export.started_at.isoformat() if export.started_at else None,
            'completed_at': export.completed_at.isoformat() if export.completed_at else None,
            'error_message': export.error_message,
            'is_completed': export.is_completed,
            'is_failed': export.is_failed,
            'is_processing': export.is_processing,
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def download_export(request, export_id):
    """Download exported file"""
    export = get_object_or_404(ExportLog, id=export_id, user=request.user)
    
    if not export.is_completed:
        messages.error(request, 'Export is not completed yet.')
        return redirect('exports:history')
    
    if not export.file_path or not os.path.exists(export.file_path):
        messages.error(request, 'Export file not found.')
        return redirect('exports:history')
    
    try:
        with open(export.file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{export.filename}"'
            return response
    except Exception as e:
        messages.error(request, f'Error downloading file: {str(e)}')
        return redirect('exports:history')


@login_required
def cancel_export_api(request, export_id):
    """API endpoint to cancel an export"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        export = get_object_or_404(ExportLog, id=export_id, user=request.user)
        
        if export.is_completed or export.is_failed:
            return JsonResponse({'error': 'Export cannot be cancelled'}, status=400)
        
        export.status = 'cancelled'
        export.completed_at = timezone.now()
        export.error_message = 'Export cancelled by user'
        export.save()
        
        return JsonResponse({
            'message': 'Export cancelled successfully',
            'status': export.status
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def delete_export_api(request, export_id):
    """API endpoint to delete an export record"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        export = get_object_or_404(ExportLog, id=export_id, user=request.user)
        
        # Delete the file if it exists
        if export.file_path and os.path.exists(export.file_path):
            try:
                os.remove(export.file_path)
            except Exception as e:
                print(f"Error deleting file {export.file_path}: {e}")
        
        export.delete()
        
        return JsonResponse({'message': 'Export deleted successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def bulk_delete_exports_api(request):
    """API endpoint to delete multiple exports"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        export_ids = data.get('export_ids', [])
        
        if not export_ids:
            return JsonResponse({'error': 'No exports selected'}, status=400)
        
        exports = ExportLog.objects.filter(id__in=export_ids, user=request.user)
        deleted_count = 0
        
        for export in exports:
            # Delete the file if it exists
            if export.file_path and os.path.exists(export.file_path):
                try:
                    os.remove(export.file_path)
                except Exception as e:
                    print(f"Error deleting file {export.file_path}: {e}")
            
            export.delete()
            deleted_count += 1
        
        return JsonResponse({
            'message': f'{deleted_count} exports deleted successfully',
            'deleted_count': deleted_count
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def export_stats_api(request):
    """API endpoint to get export statistics"""
    try:
        # Get date range from request
        days = int(request.GET.get('days', 30))
        date_from = timezone.now().date() - timedelta(days=days)
        
        # Base queryset
        exports = ExportLog.objects.filter(
            user=request.user,
            created_at__date__gte=date_from
        )
        
        # Calculate statistics
        stats = {
            'total_exports': exports.count(),
            'completed_exports': exports.filter(status='completed').count(),
            'failed_exports': exports.filter(status='failed').count(),
            'processing_exports': exports.filter(status='processing').count(),
            'total_records_exported': exports.filter(status='completed').aggregate(
                total=Sum('record_count')
            )['total'] or 0,
            'total_file_size': exports.filter(status='completed').aggregate(
                total=Sum('file_size')
            )['total'] or 0,
            'success_rate': 0,
        }
        
        if stats['total_exports'] > 0:
            stats['success_rate'] = round(
                (stats['completed_exports'] / stats['total_exports']) * 100, 1
            )
        
        # Export type distribution
        type_distribution = exports.values('export_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Daily export trend
        daily_trend = exports.extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        return JsonResponse({
            'stats': stats,
            'type_distribution': list(type_distribution),
            'daily_trend': list(daily_trend),
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def create_export_api(request):
    """API endpoint to create a new export"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        export_type = data.get('export_type')
        export_format = data.get('export_format', 'csv')
        filters = data.get('filters', {})
        
        if not export_type:
            return JsonResponse({'error': 'Export type is required'}, status=400)
        
        # Check export limits
        export_limit, created = ExportLimit.objects.get_or_create(
            user_id=str(request.user.id),
            defaults={'limit': 100}
        )
        
        if not export_limit.can_export():
            return JsonResponse({
                'error': f'Daily export limit reached ({export_limit.limit} exports)'
            }, status=429)
        
        # Create export log
        export = ExportLog.objects.create(
            user=request.user,
            export_type=export_type,
            export_format=export_format,
            filters_applied=filters,
            filename=f"{export_type}_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{export_format}",
            status='pending'
        )
        
        # Start export task
        process_export_task.delay(export.id)
        
        # Update export limit
        export_limit.export_count += 1
        export_limit.last_export_at = timezone.now()
        export_limit.save()
        
        return JsonResponse({
            'message': 'Export started successfully',
            'export_id': export.id,
            'remaining_exports': export_limit.get_remaining_exports()
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)