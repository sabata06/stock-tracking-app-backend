from django.urls import path
from .views import UserRegistrationView, PasswordChangeView,UserStatusUpdateView, UserDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
      # Kullanıcı aktif/pasif etme
    path('users/<int:pk>/status/', UserStatusUpdateView.as_view(), name='user-status-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
