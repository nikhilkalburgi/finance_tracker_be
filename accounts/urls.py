from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView # type: ignore
from . import views

urlpatterns = [
    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]