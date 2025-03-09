from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from .serializers import PasswordChangeSerializer
from .serializers import UserStatusUpdateSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Bu satırı ekleyin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.UpdateAPIView):
    """
    Allows a logged-in user to change their password.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserStatusUpdateView(generics.UpdateAPIView):
    """
    Allows an admin to set a user's is_active field to True/False.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]  # Sadece admin kullanıcılar erişebilir

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class UserDeleteView(generics.DestroyAPIView):
    """
    Allows an admin to delete a user by ID.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser]    