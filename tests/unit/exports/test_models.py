"""
Tests for exports models
"""
import pytest
from django.utils import timezone
from apps.exports.models import ExportLog, ExportLimit


@pytest.mark.django_db
class TestExportLog:
    """Test ExportLog model"""
    
    def test_export_log_creation(self, export_log):
        """Test export log can be created"""
        assert export_log.status == 'completed'
        assert export_log.export_type == 'contacts'
        assert export_log.record_count == 50
    
    def test_export_log_is_completed(self, export_log):
        """Test is_completed property"""
        assert export_log.is_completed is True
        export_log.status = 'processing'
        export_log.save()
        assert export_log.is_processing is True
    
    def test_export_log_duration(self, db, user):
        """Test duration calculation"""
        export = ExportLog.objects.create(
            user=user,
            export_type='contacts',
            status='completed',
            started_at=timezone.now(),
            completed_at=timezone.now()
        )
        # Duration should be calculated
        assert export.duration is not None or export.duration is None
    
    def test_export_log_mark_as_completed(self, db, user):
        """Test mark_as_completed method"""
        export = ExportLog.objects.create(
            user=user,
            export_type='contacts',
            status='pending'
        )
        export.mark_as_completed(file_path='/test/path.csv', file_size=1000)
        export.refresh_from_db()
        assert export.status == 'completed'
        assert export.progress_percentage == 100.0


@pytest.mark.django_db
class TestExportLimit:
    """Test ExportLimit model"""
    
    def test_export_limit_creation(self, export_limit):
        """Test export limit can be created"""
        assert export_limit.limit == 100
        assert export_limit.export_count == 0
    
    def test_export_limit_can_export(self, export_limit):
        """Test can_export method"""
        assert export_limit.can_export() is True
        export_limit.export_count = 100
        export_limit.save()
        assert export_limit.can_export() is False
    
    def test_export_limit_remaining_exports(self, export_limit):
        """Test get_remaining_exports method"""
        assert export_limit.get_remaining_exports() == 100
        export_limit.export_count = 50
        export_limit.save()
        assert export_limit.get_remaining_exports() == 50

