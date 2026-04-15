from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User  
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [] # Allow anyone to access this view (no authentication required)
    # print(queryset[0].value() if queryset else "No users found")

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"status": "This is a protected view. You are authenticated!"})