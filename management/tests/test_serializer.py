from management.serializers import ProjectSerializer, TaskSerializer, MilestoneSerializer, NotificationSerializer,UserSerializer
from rest_framework.test import APITestCase
from management.models import Project, Task, Milestone,Notification,User
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

class ProjectSerializerTest(APITestCase):
    """
    Test cases for the ProjectSerializer.
    """

    def setUp(self):
        """
        Set up a user and a project instance for testing the ProjectSerializer.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            role='admin'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.serializer = ProjectSerializer(instance=self.project)

    def test_serializer_valid(self):
        """
        Test that the serializer correctly serializes valid project data.
        """
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Project')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['owner'], self.user.id)
        self.assertIn('created_at', data)  # Check that created_at field is included in the serialized data

    def test_serializer_invalid(self):
        """
        Test that the serializer correctly handles invalid project data.
        """
        invalid_data = {'name': '', 'description': '', 'owner': 'invalid-id'}
        serializer = ProjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)  # Validate that 'name' field error is captured
        self.assertIn('description', serializer.errors)  # Validate that 'description' field error is captured
        self.assertIn('owner', serializer.errors)  # Validate that 'owner' field error is captured

class TaskSerializerTest(APITestCase):
    """
    Test cases for the TaskSerializer.
    """

    def setUp(self):
        """
        Set up a user, project, and task instance for testing the TaskSerializer.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            role='admin'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test description',
            assigned_to=self.user,
            due_date=timezone.now(),
            status='pending'
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_valid(self):
        """
        Test that the serializer correctly serializes valid task data.
        """
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Task')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['project'], self.project.id)
        self.assertEqual(data['assigned_to'], self.user.id)
        self.assertIn('due_date', data)  # Check that due_date field is included in the serialized data
        self.assertIn('created_at', data)  # Check that created_at field is included in the serialized data
        self.assertIn('updated_at', data)  # Check that updated_at field is included in the serialized data

    def test_serializer_invalid(self):
        """
        Test that the serializer correctly handles invalid task data.
        """
        invalid_data = {
            'project': 'invalid-id',
            'name': '',
            'description': '',
            'assigned_to': 'invalid-id',
            'due_date': 'invalid-date'
        }
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)  # Validate that 'name' field error is captured
        self.assertIn('description', serializer.errors)  # Validate that 'description' field error is captured
        self.assertIn('project', serializer.errors)  # Validate that 'project' field error is captured
        self.assertIn('assigned_to', serializer.errors)  # Validate that 'assigned_to' field error is captured
        self.assertIn('due_date', serializer.errors)  # Validate that 'due_date' field error is captured

class MilestoneSerializerTest(APITestCase):
    """
    Test cases for the MilestoneSerializer.
    """

    def setUp(self):
        """
        Set up a user, project, and milestone instance for testing the MilestoneSerializer.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword',
            role='admin'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.milestone = Milestone.objects.create(
            project=self.project,
            name='Test Milestone',
            description='Milestone description',
            due_date=timezone.now()
        )
        self.serializer = MilestoneSerializer(instance=self.milestone)

    def test_serializer_valid(self):
        """
        Test that the serializer correctly serializes valid milestone data.
        """
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Milestone')
        self.assertEqual(data['description'], 'Milestone description')
        self.assertEqual(data['project'], self.project.id)
        self.assertIn('due_date', data)  # Check that due_date field is included in the serialized data
        self.assertIn('created_at', data)  # Check that created_at field is included in the serialized data
        self.assertIn('updated_at', data)  # Check that updated_at field is included in the serialized data

    def test_serializer_invalid(self):
        """
        Test that the serializer correctly handles invalid milestone data.
        """
        invalid_data = {
            'project': 'invalid-id',
            'name': '',
            'description': '',
            'due_date': 'invalid-date'
        }
        serializer = MilestoneSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)  # Validate that 'name' field error is captured
        self.assertIn('description', serializer.errors)  # Validate that 'description' field error is captured
        self.assertIn('project', serializer.errors)  # Validate that 'project' field error is captured
        self.assertIn('due_date', serializer.errors)  # Validate that 'due_date' field error is captured

class NotificationSerializerTest(APITestCase):
    """
    Test cases for the NotificationSerializer.
    """

    def setUp(self):
        """
        Set up a user and a notification instance for testing the NotificationSerializer.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            role='admin'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message='Test Notification Message'
        )
        self.serializer = NotificationSerializer(instance=self.notification)

    def test_serializer_valid(self):
        """
        Test that the serializer correctly serializes valid notification data.
        """
        data = self.serializer.data
        self.assertEqual(data['message'], 'Test Notification Message')
        self.assertEqual(data['user'], self.user.id)
        self.assertIn('created_at', data)  # Check that created_at field is included in the serialized data
        self.assertIn('is_read', data)  # Check that is_read field is included in the serialized data

    def test_serializer_invalid(self):
        """
        Test that the serializer correctly handles invalid notification data.
        """
        invalid_data = {'user': 'invalid-id', 'message': '', 'created_at': 'invalid-date'}
        serializer = NotificationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)  # Validate that 'user' field error is captured
        self.assertIn('message', serializer.errors)  # Validate that 'message' field error is captured

