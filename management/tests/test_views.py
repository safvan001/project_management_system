from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from management.models import Project,Task, Milestone,Notification
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
User = get_user_model()

class ProjectViewSetTest(APITestCase):
    """
    Test cases for the Project API ViewSet.
    """

    def setUp(self):
        """
        Set up a user, obtain JWT token, and create a project instance for testing the ProjectViewSet.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='admin'
        )
        self.token = self._get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.list_url = reverse('project-list-create')
        self.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.detail_url = reverse('project-detail', kwargs={'pk': self.project.pk})

    def _get_jwt_token(self, user):
        """
        Helper method to obtain a JWT token for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_project(self):
        """
        Test that a new project can be created via the API.
        """
        data = {'name': 'New Project', 'description': 'Project description', 'owner': self.user.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_project(self):
        """
        Test that an existing project can be updated via the API.
        """
        data = {'name': 'Updated Project Name', 'description': 'Updated description', 'owner': self.user.id}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        """
        Test that an existing project can be deleted via the API.
        """
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TaskAPIViewTest(APITestCase):
    """
    Test cases for the Task API views.
    """

    def setUp(self):
        """
        Set up a user, project, and task instance for testing the Task API views.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='admin'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )
        self.token = self._get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.list_url = reverse('task-list-create')
        
        self.due_date = timezone.now() + timedelta(days=7)  # Set due date to one week from now

        self.task = Task.objects.create(
            name='Test Task',
            description='Test description',
            project=self.project,
            assigned_to=self.user,
            due_date=self.due_date
        )
        self.detail_url = reverse('task-detail', kwargs={'pk': self.task.pk})

    def _get_jwt_token(self, user):
        """
        Helper method to obtain a JWT token for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_tasks(self):
        """
        Test that tasks are listed correctly via the API.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Task')

    def test_create_task(self):
        """
        Test that a new task can be created via the API.
        """
        data = {
            'name': 'New Task',
            'description': 'Task description',
            'project': self.project.id,
            'assigned_to': self.user.id,
            'due_date': self.due_date.isoformat()  # Include due_date here
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Task')

    def test_get_task(self):
        """
        Test that a specific task can be retrieved via the API.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Task')

    def test_update_task(self):
        """
        Test that an existing task can be updated via the API.
        """
        data = {
            'name': 'Updated Task Name',
            'description': 'Updated description',
            'project': self.project.id,
            'assigned_to': self.user.id,
            'due_date': (timezone.now() + timedelta(days=15)).isoformat()  # Include due_date here
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task Name')

    def test_delete_task(self):
        """
        Test that an existing task can be deleted via the API.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

class MilestoneAPIViewTest(APITestCase):
    """
    Test cases for the Milestone API views.
    """

    def setUp(self):
        """
        Set up a user, project, and milestone instance for testing the Milestone API views.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='admin'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )
        self.token = self._get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        self.milestone = Milestone.objects.create(
            name='Test Milestone',
            description='Test milestone description',
            project=self.project,
            due_date=timezone.now() + timedelta(days=7)  # Setting a future date for the milestone
        )
        
        self.list_url = reverse('milestone-list-create')
        self.detail_url = reverse('milestone-detail', kwargs={'pk': self.milestone.pk})

    def _get_jwt_token(self, user):
        """
        Helper method to obtain a JWT token for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_milestones(self):
        """
        Test that milestones are listed correctly via the API.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Milestone')

    def test_create_milestone(self):
        """
        Test that a new milestone can be created via the API.
        """
        data = {
            'name': 'New Milestone',
            'description': 'New milestone description',
            'project': self.project.id,
            'due_date': (timezone.now() + timedelta(days=10)).isoformat()
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Milestone')

    def test_get_milestone(self):
        """
        Test that a specific milestone can be retrieved via the API.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Milestone')

    def test_update_milestone(self):
        """
        Test that an existing milestone can be updated via the API.
        """
        data = {
            'name': 'Updated Milestone Name',
            'description': 'Updated milestone description',
            'project': self.project.id,
            'due_date': (timezone.now() + timedelta(days=15)).isoformat()
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Milestone Name')

    def test_delete_milestone(self):
        """
        Test that an existing milestone can be deleted via the API.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Milestone.objects.count(), 0)

class NotificationAPIViewTest(APITestCase):
    """
    Test cases for the Notification API views.
    """

    def setUp(self):
        """
        Set up a user and a notification instance for testing the Notification API views.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='admin'
        )
        self.token = self._get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        self.notification = Notification.objects.create(
            user=self.user,
            message='Test Notification Message',
            created_at=timezone.now()
        )
        
        self.list_url = reverse('notification-list-create')

    def _get_jwt_token(self, user):
        """
        Helper method to obtain a JWT token for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_notifications(self):
        """
        Test that notifications are listed correctly via the API.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Test Notification Message')

    def test_create_notification(self):
        """
        Test that a new notification can be created via the API.
        """
        data = {
            'user': self.user.id,
            'message': 'New Notification Message',
            'created_at': timezone.now().isoformat()
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'New Notification Message')

