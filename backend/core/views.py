from rest_framework import viewsets
from .models import User, Team
from .serializers import UserSerializer, TeamSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_employee(self, request, pk=None):
        team = self.get_object()
        employee_id = request.data.get('employee_id')
        employee = User.objects.get(id=employee_id)
        team.employees.add(employee)
        return Response({'status': 'employee added'})

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=400)
