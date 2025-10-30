"""
Tests for the Progress Tracker functionality
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from apps.core.models import TaskCategory, TaskTracker
import json


class ProgressTrackerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test categories
        self.category1 = TaskCategory.objects.create(
            name='Setup & Configuration',
            description='Initial setup tasks',
            color='#007bff',
            icon='fas fa-cog',
            order=1
        )
        
        self.category2 = TaskCategory.objects.create(
            name='Core Features',
            description='Main application features',
            color='#28a745',
            icon='fas fa-star',
            order=2
        )
        
        # Create test tasks
        self.task1 = TaskTracker.objects.create(
            category=self.category1,
            task_name='Database Setup',
            description='Configure database connection',
            priority='HIGH',
            order=1
        )
        
        self.task2 = TaskTracker.objects.create(
            category=self.category1,
            task_name='User Authentication',
            description='Implement user login system',
            priority='CRITICAL',
            order=2,
            is_completed=True,
            completed_at=timezone.now()
        )
        
        self.task3 = TaskTracker.objects.create(
            category=self.category2,
            task_name='Contact Management',
            description='Create contact CRUD operations',
            priority='HIGH',
            order=1
        )

    def test_progress_tracker_view(self):
        """Test the progress tracker page loads correctly"""
        response = self.client.get(reverse('core:progress_tracker'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project Progress Tracker')
        self.assertContains(response, 'Database Setup')
        self.assertContains(response, 'User Authentication')

    def test_categories_api(self):
        """Test the categories API endpoint"""
        response = self.client.get(reverse('core:categories_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('categories', data)
        self.assertEqual(len(data['categories']), 2)
        
        # Check category data structure
        category = data['categories'][0]
        self.assertIn('id', category)
        self.assertIn('name', category)
        self.assertIn('description', category)
        self.assertIn('color', category)
        self.assertIn('icon', category)
        self.assertIn('progress_percentage', category)

    def test_tasks_api(self):
        """Test the tasks API endpoint"""
        response = self.client.get(reverse('core:tasks_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('tasks', data)
        self.assertEqual(len(data['tasks']), 3)
        
        # Check task data structure
        task = data['tasks'][0]
        self.assertIn('id', task)
        self.assertIn('task_name', task)
        self.assertIn('description', task)
        self.assertIn('priority', task)
        self.assertIn('is_completed', task)
        self.assertIn('category', task)

    def test_update_task_status_api(self):
        """Test updating task completion status"""
        # Test marking task as completed
        response = self.client.post(
            reverse('core:update_task_status_api', args=[self.task1.id]),
            {'is_completed': 'true'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['is_completed'])
        
        # Verify task was updated in database
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)
        self.assertIsNotNone(self.task1.completed_at)
        
        # Test marking task as incomplete
        response = self.client.post(
            reverse('core:update_task_status_api', args=[self.task1.id]),
            {'is_completed': 'false'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['is_completed'])
        
        # Verify task was updated in database
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_completed)
        self.assertIsNone(self.task1.completed_at)

    def test_progress_stats_api(self):
        """Test the progress statistics API"""
        response = self.client.get(reverse('core:progress_stats_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('overall_progress', data)
        self.assertIn('total_tasks', data)
        self.assertIn('completed_tasks', data)
        self.assertIn('remaining_tasks', data)
        self.assertIn('categories', data)
        
        # Check overall progress calculation
        self.assertEqual(data['total_tasks'], 3)
        self.assertEqual(data['completed_tasks'], 1)
        self.assertEqual(data['remaining_tasks'], 2)
        self.assertAlmostEqual(data['overall_progress'], 33.3, places=1)

    def test_category_completion_percentage(self):
        """Test category completion percentage calculation"""
        # Category 1 has 2 tasks, 1 completed (50%)
        self.assertEqual(self.category1.completion_percentage, 50.0)
        
        # Category 2 has 1 task, 0 completed (0%)
        self.assertEqual(self.category2.completion_percentage, 0.0)
        
        # Complete the remaining task in category 1
        self.task1.is_completed = True
        self.task1.completed_at = timezone.now()
        self.task1.save()
        
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.completion_percentage, 100.0)

    def test_task_model_properties(self):
        """Test TaskTracker model properties"""
        # Test completed task
        self.assertTrue(self.task2.is_completed)
        self.assertFalse(self.task2.is_failed)
        self.assertIsNotNone(self.task2.completed_at)
        
        # Test incomplete task
        self.assertFalse(self.task1.is_completed)
        self.assertIsNone(self.task1.completed_at)

    def test_task_category_properties(self):
        """Test TaskCategory model properties"""
        self.assertEqual(self.category1.total_tasks_count, 2)
        self.assertEqual(self.category1.completed_tasks_count, 1)
        self.assertEqual(self.category2.total_tasks_count, 1)
        self.assertEqual(self.category2.completed_tasks_count, 0)

    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access progress tracker"""
        self.client.logout()
        
        response = self.client.get(reverse('core:progress_tracker'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        response = self.client.get(reverse('core:categories_api'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_invalid_task_update(self):
        """Test updating non-existent task"""
        response = self.client.post(
            reverse('core:update_task_status_api', args=[99999]),
            {'is_completed': 'true'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_task_ordering(self):
        """Test that tasks are ordered correctly"""
        response = self.client.get(reverse('core:tasks_api'))
        data = json.loads(response.content)
        
        tasks = data['tasks']
        # Tasks should be ordered by order, priority, task_name
        self.assertEqual(tasks[0]['task_name'], 'Database Setup')
        self.assertEqual(tasks[1]['task_name'], 'User Authentication')
        self.assertEqual(tasks[2]['task_name'], 'Contact Management')
