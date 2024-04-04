from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout

from .models import CustomUser, UserData
from .serializers import CustomUserSerializer, LoginSerializer, UserDataSerializer

class UserViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        if not serializer.data:
            return Response(
                {"message": "No users found", 'code': 200},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "fetch successful", 'data': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        email = request.data.get('email')
        if CustomUser.objects.filter(email = email).exists():
            return Response({"message": "User already exists", 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        validated_data = serializer.validated_data
        CustomUser.objects.create_user(**validated_data)
        return Response(
            {"message": "User created successfully", 'code': 201},
            status=status.HTTP_201_CREATED
        )

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response(
                {"message": "Invalid credentials", 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(user)
        if login(request, user):
            return Response(
                {"message": "Login successful", 'code': 200},
                status=status.HTTP_200_OK)

        return Response(
            {"message": "Login failed", 'code': 400},
            status=status.HTTP_400_BAD_REQUEST
        )

class LogoutViewset(viewsets.ViewSet):
    def create(self, request):
        print(request.user)
        logout(request)
        return Response(
            {"message": "Logout successful", 'code': 200},
            status=status.HTTP_200_OK
        )

class UserDataViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'code':200}, status=status.HTTP_201_CREATED)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = request.data.get('user')
        try:
            user_data = UserData.objects.filter(user=user)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data, many=True)
        return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user_data = UserData.objects.get(pk=pk)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data)
        return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            user_data = UserData.objects.get(pk=pk)
        except UserData.DoesNotExist:
            return Response({'data': 'Profile not found', 'code': 404}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDataSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)
        return Response({'data': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        UserData.objects.get(pk=pk).delete()
        return Response({'data': 'Profile deleted', 'code': 200}, status=status.HTTP_200_OK)
