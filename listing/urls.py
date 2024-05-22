
from django.urls import path,include
from .views import RegistrationView,ListingView,ProfileView,TransactionView,LoginApiView,LogoutApiView,UserListingView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listings',ListingView)
router.register(r'transactions',TransactionView)

urlpatterns = [
    path("register/",RegistrationView.as_view(),name="register"),
    path("login/",LoginApiView.as_view(),name="login"),
    path("logout/",LogoutApiView.as_view(),name="logout"),
    path("profile/<int:pk>/",ProfileView.as_view(),name="profile"),
    path("user_listing/",UserListingView.as_view(),name="user_listing")
]
urlpatterns += router.urls