from django.urls import path, include
from .views import (
    CountUsers,
    Register,
    DeleteUser,
    PutUser,
    ChangePassword,
    UserViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("count/users/", CountUsers.as_view()),
    path("register/", Register.as_view()),
    path("alter/user/", PutUser.as_view()),
    path("change/password/", ChangePassword.as_view()),
    path("delete/", DeleteUser.as_view()),
]
