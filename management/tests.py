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
class UserModelTest(TestCase):
    """
    Test cases for the User model.
    """

    def setUp(self):
        """
        Set up a user instance for testing.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
            role='admin'
        )

    def test_user_creation(self):
        """
        Test that the user is created correctly with the expected username, role,
        and hashed password.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'admin')
        self.assertTrue(self.user.check_password('password'))

    def test_user_role_choices(self):
        """
        Test that the user's role is within the defined choices.
        """
        roles = dict(self.user.Roles)
        self.assertIn(self.user.role, roles)

class ProjectModelTest(TestCase):
    """
    Test cases for the Project model.
    """

    def setUp(self):
        """
        Set up a user and a project instance for testing.
        """
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
        """
        Test that the project is created correctly with the expected name,
        description, and owner.
        """
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test Description')
        self.assertEqual(self.project.owner, self.user)

    def test_project_owner(self):
        """
        Test that the project's owner is correctly set.
        """
        self.assertEqual(self.project.owner.username, 'testuser')

class TaskModelTest(TestCase):
    """
    Test cases for the Task model.
    """

    def setUp(self):
        """
        Set up a user, a project, and a task instance for testing.
        """
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
        """
        Test that the task is created correctly with the expected project, name,
        description, assigned user, due date, and status.
        """
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Task Description')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertEqual(self.task.due_date, datetime(2024, 12, 31, 23, 59))
        self.assertEqual(self.task.status, 'pending')

    def test_task_status_choices(self):
        """
        Test that the task status can be updated to 'completed' and saved correctly.
        """
        self.task.status = 'completed'
        self.task.save()
        self.assertEqual(self.task.status, 'completed')

class MilestoneModelTest(TestCase):
    """
    Test cases for the Milestone model.
    """

    def setUp(self):
        """
        Set up a user, a project, and a milestone instance for testing.
        """
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
        """
        Test that the milestone is created correctly with the expected project, name,
        description, and due date.
        """
        self.assertEqual(self.milestone.name, 'Test Milestone')
        self.assertEqual(self.milestone.description, 'Test Milestone Description')
        self.assertEqual(self.milestone.project, self.project)
        self.assertEqual(self.milestone.due_date, datetime(2024, 12, 31, 23, 59))

    def test_milestone_dates(self):
        """
        Test that the milestone has valid created_at and updated_at timestamps.
        """
        self.assertTrue(self.milestone.created_at)
        self.assertTrue(self.milestone.updated_at)

class NotificationModelTest(TestCase):
    """
    Test cases for the Notification model.
    """

    def setUp(self):
        """
        Set up a user and a notification instance for testing.
        """
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
        """
        Test that the notification is created correctly with the expected user,
        message, and read status.
        """
        self.assertEqual(self.notification.message, 'Test Notification')
        self.assertEqual(self.notification.user, self.user)
        self.assertFalse(self.notification.is_read)

    def test_notification_is_read(self):
        """
        Test that the notification's read status can be updated and saved correctly.
        """
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)

