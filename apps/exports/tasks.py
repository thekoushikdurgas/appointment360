"""
Export tasks for background processing
"""
import os
import csv
import json
import pandas as pd
from datetime import datetime
from django.conf import settings
from celery import shared_task
from django.utils import timezone
from .models import ExportLog
from apps.contacts.models import Contact


@shared_task
def process_export_task(export_id):
    """Process export task in background"""
    try:
        export = ExportLog.objects.get(id=export_id)
        export.mark_as_started()
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        # Generate filename
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{export.export_type}_{timestamp}.{export.export_format}"
        file_path = os.path.join(exports_dir, filename)
        
        # Process based on export type
        if export.export_type == 'contacts':
            success = export_contacts(export, file_path)
        elif export.export_type == 'bulk_export':
            success = export_bulk_contacts(export, file_path)
        elif export.export_type == 'selected_contacts':
            success = export_selected_contacts(export, file_path)
        elif export.export_type == 'analytics':
            success = export_analytics(export, file_path)
        else:
            success = False
            export.mark_as_failed("Unsupported export type")
        
        if success:
            # Get file size
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            # Update export record
            export.mark_as_completed(file_path=file_path, file_size=file_size)
            export.filename = filename
            export.save()
        else:
            export.mark_as_failed("Export processing failed")
    
    except ExportLog.DoesNotExist:
        print(f"Export {export_id} not found")
    except Exception as e:
        print(f"Error processing export {export_id}: {str(e)}")
        try:
            export = ExportLog.objects.get(id=export_id)
            export.mark_as_failed(str(e))
        except:
            pass


def export_contacts(export, file_path):
    """Export all contacts"""
    try:
        # Apply filters if any
        contacts = Contact.objects.filter(user=export.user)
        
        filters = export.filters_applied
        if filters:
            if filters.get('status'):
                contacts = contacts.filter(status=filters['status'])
            if filters.get('industry'):
                contacts = contacts.filter(industry=filters['industry'])
            if filters.get('country'):
                contacts = contacts.filter(country=filters['country'])
            if filters.get('date_from'):
                contacts = contacts.filter(created_at__date__gte=filters['date_from'])
            if filters.get('date_to'):
                contacts = contacts.filter(created_at__date__lte=filters['date_to'])
        
        # Convert to DataFrame
        data = []
        for contact in contacts:
            data.append({
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone': contact.phone,
                'company': contact.company,
                'job_title': contact.job_title,
                'industry': contact.industry,
                'country': contact.country,
                'city': contact.city,
                'status': contact.status,
                'created_at': contact.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': contact.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        df = pd.DataFrame(data)
        
        # Export based on format
        if export.export_format == 'csv':
            df.to_csv(file_path, index=False)
        elif export.export_format == 'excel':
            df.to_excel(file_path, index=False)
        elif export.export_format == 'json':
            df.to_json(file_path, orient='records', indent=2)
        
        # Update record count
        export.record_count = len(data)
        export.save()
        
        return True
    
    except Exception as e:
        print(f"Error exporting contacts: {str(e)}")
        return False


def export_bulk_contacts(export, file_path):
    """Export contacts based on bulk selection"""
    try:
        contact_ids = export.filters_applied.get('contact_ids', [])
        
        if not contact_ids:
            return False
        
        contacts = Contact.objects.filter(id__in=contact_ids, user=export.user)
        
        # Convert to DataFrame
        data = []
        for contact in contacts:
            data.append({
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone': contact.phone,
                'company': contact.company,
                'job_title': contact.job_title,
                'industry': contact.industry,
                'country': contact.country,
                'city': contact.city,
                'status': contact.status,
                'created_at': contact.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': contact.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        df = pd.DataFrame(data)
        
        # Export based on format
        if export.export_format == 'csv':
            df.to_csv(file_path, index=False)
        elif export.export_format == 'excel':
            df.to_excel(file_path, index=False)
        elif export.export_format == 'json':
            df.to_json(file_path, orient='records', indent=2)
        
        # Update record count
        export.record_count = len(data)
        export.save()
        
        return True
    
    except Exception as e:
        print(f"Error exporting bulk contacts: {str(e)}")
        return False


def export_selected_contacts(export, file_path):
    """Export selected contacts (same as bulk for now)"""
    return export_bulk_contacts(export, file_path)


def export_analytics(export, file_path):
    """Export analytics data"""
    try:
        # This would export analytics data
        # For now, just create a placeholder file
        analytics_data = {
            'export_type': 'analytics',
            'timestamp': timezone.now().isoformat(),
            'data': 'Analytics export placeholder'
        }
        
        if export.export_format == 'json':
            with open(file_path, 'w') as f:
                json.dump(analytics_data, f, indent=2)
        elif export.export_format == 'csv':
            # Convert to CSV format
            df = pd.DataFrame([analytics_data])
            df.to_csv(file_path, index=False)
        
        export.record_count = 1
        export.save()
        
        return True
    
    except Exception as e:
        print(f"Error exporting analytics: {str(e)}")
        return False
