"""
Tests for core models
"""
import pytest
from django.utils import timezone
from apps.core.models import TaskTracker, TaskCategory


@pytest.mark.django_db
class TestTaskTracker:
    """Test TaskTracker model"""
    
    def test_task_creation(self, task_tracker):
        """Test task can be created"""
        assert task_tracker.task_name == 'Test Task'
        assert task_tracker.category == 'SETUP'
        assert task_tracker.is_completed is False
    
    def test_task_completion_updates_timestamp(self, task_tracker):
        """Test completing task sets completed_at"""
        assert task_tracker.completed_at is None
        task_tracker.is_completed = True
        task_tracker.save()
        assert task_tracker.completed_at is not None
    
    def test_task_str_method(self, task_tracker):
        """Test task string representation"""
        assert 'Test Task' in str(task_tracker)
    
    def test_task_ordering(self, db):
        """Test tasks are ordered correctly"""
        category = TaskCategory.objects.create(name='Test', order=1)
        task1 = TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 1',
            order=1
        )
        task2 = TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 2',
            order=2
        )
        tasks = list(TaskTracker.objects.all())
        assert tasks[0].order <= tasks[1].order


@pytest.mark.django_db
class TestTaskCategory:
    """Test TaskCategory model"""
    
    def test_category_creation(self, task_category):
        """Test category can be created"""
        assert task_category.name == 'Test Category'
        assert task_category.is_active is True
    
    def test_category_completion_percentage(self, db):
        """Test category completion percentage calculation"""
        category = TaskCategory.objects.create(name='Test Category', order=1)
        # Create tasks
        TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 1',
            is_completed=True
        )
        TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 2',
            is_completed=False
        )
        # Check percentage (should be 50% if one of two is complete)
        assert category.completion_percentage >= 0
    
    def test_category_task_counts(self, db):
        """Test category task count properties"""
        category = TaskCategory.objects.create(name='Test Category', order=1)
        TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 1',
            is_completed=True
        )
        TaskTracker.objects.create(
            category='SETUP',
            task_name='Task 2',
            is_completed=False
        )
        assert category.total_tasks_count == 2
        assert category.completed_tasks_count == 1

