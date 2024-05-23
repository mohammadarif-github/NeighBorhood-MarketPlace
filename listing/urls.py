from django.urls import path, include
from .views import RegistrationView, ListingView, ProfileView, TransactionView, LoginApiView, LogoutApiView, UserListingView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'listings', ListingView)
router.register(r'transactions', TransactionView)

urlpatterns = [
    path('api/token/', LoginApiView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutApiView.as_view(), name='logout'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginApiView.as_view(), name='login'),
    path('api/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('api/user_listing/', UserListingView.as_view(), name='user_listing'),
    path('api/',include(router.urls)),
]

# Including router URLs
urlpatterns += router.urls