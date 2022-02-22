# -*- coding: UTF-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from api.settings import EMAIL_HOST_USER
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializer import UserSerializer
from .permissions import IsNotDeletedUser, ReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().filter(soft_delet=None)
    serializer_class = UserSerializer

    permission_classes = [IsNotDeletedUser]
    authentication_classes = [JWTAuthentication, TokenAuthentication]


class CountUsers(APIView):
    permission_classes = [ReadOnly]

    def get(self, request):
        qtd_users = User.objects.all().count()

        return Response({"sucess": True, "num_users": qtd_users}, 200)


class Register(APIView):
    def post(self, request):
        for field in ["email", "password"]:
            if not field in request.data:
                return Response(
                    {"sucess": False, "error": f"Campo {field} necessario"}, 406
                )

        u = User()

        if User.objects.filter(email=request.data["email"]).exists():
            if not User.objects.filter(email=request.data["email"]).first().soft_delet:
                return Response(
                    {
                        "sucess": False,
                        "error": f"Usuario com esse email já existente",
                    },
                    409,
                )
            else:
                u = User.objects.all().get(email=request.data["email"])

        u.soft_delet = None
        u.is_active = True

        for field in request.data:
            if (
                field != "password"
                and field != "is_staff"
                and field != "is_active"
                and field != "soft_delet"
            ):
                setattr(u, field, request.data[field])
        u.set_password(request.data["password"])
        u.save()

        return Response({"sucess": True, "message": "Usuario criado com sucesso"}, 201)


class PutUser(APIView):
    def put(self, request):
        protected_fields = [
            "is_staff",
            "is_active",
            "soft_delet",
            "password",
        ]

        user = request.user
        for field in request.data:
            if not field in protected_fields:
                setattr(user, field, request.data[field])
        user.save()

        return Response(
            {"sucess": True, "message": "Usuario atualizado com sucesso"}, 200
        )

    permission_classes = [IsNotDeletedUser]
    authentication_classes = [JWTAuthentication]


class ChangePassword(APIView):
    def post(self, request):
        if not "password" in request.data:
            return Response({"sucess": False, "error": "Senha necessária"}, 406)
        if not "new_password" in request.data:
            return Response({"sucess": False, "error": "Senha necessária"}, 406)

        user = request.user
        if user.check_password(request.data["password"]):
            user.set_password(request.data["new_password"])
            user.save()
            return Response(
                {"sucess": True, "message": "Senha alterada com sucesso"}, 200
            )
        else:
            return Response({"sucess": False, "error": "Senha incorreta"}, 401)

    permission_classes = [IsNotDeletedUser]
    authentication_classes = [JWTAuthentication]


class DeleteUser(APIView):
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.is_trusty = None
        user.soft_delet = timezone.now()
        user.save()
        return Response(
            {"sucess": True, "message": "Usuario deletado com sucesso"}, 200
        )

    permission_classes = [IsNotDeletedUser]
    authentication_classes = [JWTAuthentication]
