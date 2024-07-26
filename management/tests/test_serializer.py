from management.serializers import ProjectSerializer, TaskSerializer, MilestoneSerializer, NotificationSerializer,UserSerializer
from rest_framework.test import APITestCase
from management.models import Project, Task, Milestone,Notification,User
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

class ProjectSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test description', owner=self.user)
        self.serializer = ProjectSerializer(instance=self.project)

    def test_serializer_valid(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Project')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['owner'], self.user.id)
        self.assertIn('created_at', data)  

    def test_serializer_invalid(self):
        invalid_data = {'name': '', 'description': '', 'owner': 'invalid-id'}
        serializer = ProjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('owner', serializer.errors)

class TaskSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword', role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test description', owner=self.user)
        self.task = Task.objects.create(
            project=self.project, name='Test Task', description='Test description',
            assigned_to=self.user, due_date=timezone.now(), status='pending'
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_valid(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Task')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['project'], self.project.id)
        self.assertEqual(data['assigned_to'], self.user.id)
        self.assertIn('due_date', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_serializer_invalid(self):
        invalid_data = {'project': 'invalid-id', 'name': '', 'description': '', 'assigned_to': 'invalid-id', 'due_date': 'invalid-date'}
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('project', serializer.errors)
        self.assertIn('assigned_to', serializer.errors)
        self.assertIn('due_date', serializer.errors)

class MilestoneSerializerTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword', role='admin')
        self.project = Project.objects.create(name='Test Project', description='Test description', owner=self.user)
        self.milestone = Milestone.objects.create(
            project=self.project, name='Test Milestone', description='Milestone description',
            due_date=timezone.now()
        )
        self.serializer = MilestoneSerializer(instance=self.milestone)

    def test_serializer_valid(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Milestone')
        self.assertEqual(data['description'], 'Milestone description')
        self.assertEqual(data['project'], self.project.id)
        self.assertIn('due_date', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_serializer_invalid(self):
        invalid_data = {
            'project': 'invalid-id',
            'name': '',  
            'description': '',  
            'due_date': 'invalid-date' 
        }
        serializer = MilestoneSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('description', serializer.errors)
        self.assertIn('project', serializer.errors)
        self.assertIn('due_date', serializer.errors)

class NotificationSerializerTest(APITestCase):
    
    def setUp(self):
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
        data = self.serializer.data
        self.assertEqual(data['message'], 'Test Notification Message')
        self.assertEqual(data['user'], self.user.id)
        self.assertIn('created_at', data)
        self.assertIn('is_read', data) 

    def test_serializer_invalid(self):
        invalid_data = {'user': 'invalid-id', 'message': '', 'created_at': 'invalid-date'}
        serializer = NotificationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertIn('message', serializer.errors)

