from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from management.models import Project, Task, Milestone,Notification
from management.serializers import ProjectSerializer, TaskSerializer
from rest_framework.test import APIClient
from datetime import datetime



User = get_user_model()
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
            role='admin'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'admin')
        self.assertTrue(self.user.check_password('password'))

    def test_user_role_choices(self):
        roles = dict(self.user.Roles)
        self.assertIn(self.user.role, roles)

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test Description')
        self.assertEqual(self.project.owner, self.user)

    def test_project_owner(self):
        self.assertEqual(self.project.owner.username, 'testuser')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )
        self.task = Task.objects.create(
            project=self.project,
            name='Test Task',
            description='Test Task Description',
            assigned_to=self.user,
            due_date=datetime(2024, 12, 31, 23, 59),
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Task Description')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertEqual(self.task.due_date, datetime(2024, 12, 31, 23, 59))
        self.assertEqual(self.task.status, 'pending')

    def test_task_status_choices(self):
        self.task.status = 'completed'
        self.task.save()
        self.assertEqual(self.task.status, 'completed')

class MilestoneModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )
        self.milestone = Milestone.objects.create(
            project=self.project,
            name='Test Milestone',
            description='Test Milestone Description',
            due_date=datetime(2024, 12, 31, 23, 59),
        )

    def test_milestone_creation(self):
        self.assertEqual(self.milestone.name, 'Test Milestone')
        self.assertEqual(self.milestone.description, 'Test Milestone Description')
        self.assertEqual(self.milestone.project, self.project)
        self.assertEqual(self.milestone.due_date, datetime(2024, 12, 31, 23, 59))

    def test_milestone_dates(self):
        self.assertTrue(self.milestone.created_at)
        self.assertTrue(self.milestone.updated_at)

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message='Test Notification',
            is_read=False
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.message, 'Test Notification')
        self.assertEqual(self.notification.user, self.user)
        self.assertFalse(self.notification.is_read)

    def test_notification_is_read(self):
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)


# Model Tests
# class ProjectViewSetTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='admin', password='password', role='admin')
#         self.client.force_authenticate(user=self.user)
    
#     def test_create_project(self):
#         url = reverse('project-list-create')
#         data = {
#             'name': 'New Project',
#             'description': 'Project description',
#             'owner': self.user.id
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
#     def test_get_projects(self):
#         url = reverse('project-list-create')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# class TaskViewSetTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='admin', password='password', role='admin')
#         self.client.force_authenticate(user=self.user)
    
#     def test_create_task(self):
#         url = reverse('task-list-create')
#         data = {
#             'name': 'New Task',
#             'project': 1,
#             'assigned_to': self.user.id,
#             'due_date': '2024-12-31T23:59:00Z',
#             'status': 'pending'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
#     def test_get_tasks(self):
#         url = reverse('task-list-create')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class MilestoneModelTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password123')
#         self.project = Project.objects.create(
#             name='Test Project',
#             owner=self.user
#         )
#         self.milestone = Milestone.objects.create(
#             name='Test Milestone',
#             project=self.project,
#             due_date='2024-12-31 23:59'
#         )

#     def test_milestone_creation(self):
#         self.assertEqual(self.milestone.name, 'Test Milestone')
#         self.assertEqual(self.milestone.project.name, 'Test Project')

# # View Tests
# class ProjectViewSetTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpass', role='admin')
#         self.token = self._get_jwt_token(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

#         self.project = Project.objects.create(name='Test Project', owner=self.user)
#         self.project_url = reverse('project-list')  # Adjust as needed
#         self.project_detail_url = reverse('project-detail', args=[self.project.id])  # Adjust as needed

#     def _get_jwt_token(self, user):
#         payload = api_settings.JWT_PAYLOAD_HANDLER(user)
#         token = api_settings.JWT_ENCODE_HANDLER(payload)
#         return token

#     def test_create_project(self):
#         data = {'name': 'New Project', 'description': 'New project description'}
#         response = self.client.post(self.project_url, data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Project.objects.count(), 2)
#         self.assertEqual(Project.objects.latest('id').name, 'New Project')

#     def test_get_projects(self):
#         response = self.client.get(self.project_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)  # Adjust if you have multiple projects

#     def test_get_project_detail(self):
#         response = self.client.get(self.project_detail_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['name'], 'Test Project')

#     def test_update_project(self):
#         data = {'name': 'Updated Project Name'}
#         response = self.client.put(self.project_detail_url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Project.objects.get(id=self.project.id).name, 'Updated Project Name')

#     def test_delete_project(self):
#         response = self.client.delete(self.project_detail_url)
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Project.objects.count(), 0)


# class TaskViewSetTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpass', role='admin')
#         self.token = self._get_jwt_token(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

#         self.project = Project.objects.create(name='Test Project', owner=self.user)
#         self.task = Task.objects.create(name='Test Task', project=self.project, assigned_to=self.user, due_date='2024-12-31')
#         self.task_url = reverse('task-list')  # Adjust as needed
#         self.task_detail_url = reverse('task-detail', args=[self.task.id])  # Adjust as needed

#     def _get_jwt_token(self, user):
#         payload = api_settings.JWT_PAYLOAD_HANDLER(user)
#         token = api_settings.JWT_ENCODE_HANDLER(payload)
#         return token

#     def test_create_task(self):
#         data = {'name': 'New Task', 'project': self.project.id, 'assigned_to': self.user.id, 'due_date': '2024-12-31 23:59'}
#         response = self.client.post(self.task_url, data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Task.objects.count(), 2)
#         self.assertEqual(Task.objects.latest('id').name, 'New Task')

#     def test_get_tasks(self):
#         response = self.client.get(self.task_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)  # Adjust if you have multiple tasks

#     def test_get_task_detail(self):
#         response = self.client.get(self.task_detail_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['name'], 'Test Task')

#     def test_update_task(self):
#         data = {'name': 'Updated Task Name'}
#         response = self.client.put(self.task_detail_url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Task.objects.get(id=self.task.id).name, 'Updated Task Name')

#     def test_delete_task(self):
#         response = self.client.delete(self.task_detail_url)
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Task.objects.count(), 0)


# # Serializer Tests
# class ProjectSerializerTest(TestCase):
#     def setUp(self):
#         self.project = Project.objects.create(name='Test Project', owner=self.user)
#         self.serializer = ProjectSerializer(instance=self.project)

#     def test_serializer_contains_expected_fields(self):
#         data = self.serializer.data
#         expected_fields = set(['id', 'name', 'description', 'created_at', 'updated_at', 'owner'])
#         self.assertEqual(set(data.keys()), expected_fields)

# class TaskSerializerTest(TestCase):
#     def setUp(self):
#         self.task = Task.objects.create(name='Test Task', project=self.project, assigned_to=self.user, due_date='2024-12-31')
#         self.serializer = TaskSerializer(instance=self.task)

#     def test_serializer_contains_expected_fields(self):
#         data = self.serializer.data
#         expected_fields = set(['id', 'name', 'project', 'assigned_to', 'due_date', 'created_at', 'updated_at', 'status'])
#         self.assertEqual(set(data.keys()), expected_fields)


# Create your tests here.
