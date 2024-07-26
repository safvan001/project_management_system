from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,generics,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Task, Milestone, Notification
from .serializers import ProjectSerializer, TaskSerializer, MilestoneSerializer, NotificationSerializer,UserSerializer
from .permissions import IsAdminOrManagerOrReadOnly, IsAdminOrManager, IsAdminOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from management.tasks import send_notification_email
User=get_user_model()

class UserSignUp(generics.CreateAPIView):
    """
    View to handle user sign-up.
    Allows any user to sign Up.

    """
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[AllowAny]

class LoginView(APIView):
    """
    View to handle user login.
    Authenticates user and provides JWT tokens.

    """
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        if not username or not password:
            return Response({'detail': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return Response ({'error':'User Doesn\'t Exist with the Username'}, status=status.HTTP_401_UNAUTHORIZED)

        if password==user.password:
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Authentication successful',
                'refresh': str(refresh),
                'access':str(refresh.access_token)
            },status=status.HTTP_200_OK) 
        else:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class ProjectListCreateAPIView(APIView):
    """
    View to list and create projects.
    Only admins and managers can create projects.

    """
    permission_classes = [IsAdminOrManagerOrReadOnly]
    @method_decorator(cache_page(60*2))  # Cache for 2 minutes
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project=serializer.save()
            send_notification_email.delay(
                project.owner.email,
                f'New project "{project.name}" has been created.'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailAPIView(APIView):
    """
    View to retrieve, update, or delete a project.
    Only admins and managers can update or delete projects.

    """
    permission_classes = [IsAdminOrManagerOrReadOnly]
    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            project=serializer.save()
            send_notification_email.delay(
                project.owner.email,
                f'New project "{project.name}" has been created.'
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListCreateAPIView(APIView):
    """
    View to list and create tasks.
    Only admins and managers can create tasks.
    """
    permission_classes = [IsAdminOrManager]

    @method_decorator(cache_page(60*2))  # Cache for 2 minutes
    def get(self, request):
        tasks = Task.objects.select_related('project', 'assigned_to').all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task=serializer.save()
            send_notification_email.delay(
                task.assigned_to.email,
                f'New task "{task.name}" has been assigned to you.'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
    """
    View to retrieve, update, or delete a task.
    Only admins and managers can update or delete tasks.
    """
    permission_classes = [IsAdminOrManager]

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            task=serializer.save()
            send_notification_email.delay(
                task.assigned_to.email,
                f'New task "{task.name}" has been Updated to you.'
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MilestoneListCreateAPIView(APIView):
    """
    View to list and create milestones.
    Only admins and managers can create milestones.
    """
    permission_classes = [IsAdminOrManagerOrReadOnly]

    @method_decorator(cache_page(60*2))  # Cache for 2 minutes
    def get(self, request):
        milestones = Milestone.objects.select_related('project').all()
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
            milestone=serializer.save()
            send_notification_email.delay(
                milestone.project.owner.email,
                f'New Milestone "{milestone.name}" has been created.'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MilestoneDetailAPIView(APIView):
    """
    View to retrieve, update, or delete a milestone.
    Only admins and managers can update or delete milestones.
    """
    permission_classes = [IsAdminOrManagerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Milestone, pk=pk)

    def get(self, request, pk):
        milestone = self.get_object(pk)
        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data)

    def put(self, request, pk):
        milestone = self.get_object(pk)
        serializer = MilestoneSerializer(milestone, data=request.data)
        if serializer.is_valid():
            milestone=serializer.save()
            send_notification_email.delay(
                milestone.project.owner.email,
                f'Milestone "{milestone.name}" has been Updated.'
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        milestone = self.get_object(pk)
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60*2)) 
    def get(self, request):
        notifications = Notification.objects.select_related('user').all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
