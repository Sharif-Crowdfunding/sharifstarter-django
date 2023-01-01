from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from project.serializers import *
from utils.web3provider import get_provider


# Create your views here.
class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basic_info_serializer = ProjectBasicInfoSerializer(data=request.data['basic_info'])
        basic_info_serializer.is_valid(raise_exception=True)

        token_info_serializer = ProjectTokenInfoSerializer(data=request.data['token_info'])
        token_info_serializer.is_valid(raise_exception=True)

        basic_info = basic_info_serializer.save()
        token_info = token_info_serializer.save()

        p = Project(user=request.user, name=serializer.validated_data['name'], image=serializer.validated_data['image'],
                    basic_info=basic_info, token_info=token_info)
        p.save()

        # call async function
        # get_provider().deploy_project_contract(p.user.wallet.address,p.user.wallet.encrypted_private_key,p.user.password, p.name, p.token_info.symbol,
        #                                        p.token_info.total_supply)
        return Response(ProjectSerializer(p).data)


class GetProjectInfo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id = int(request.data['id'])
        p = Project.objects.get(id=id)
        return Response(ProjectSerializer(p).data)


class CancelProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        project = Project.objects.get(id=id)
        if project:
            if project.user != user:
                return Response(status=HTTP_401_UNAUTHORIZED)
            if project.token_info.development_stage != DevelopmentStages.Inception.value:
                return Response(data={"stage error"}, status=HTTP_412_PRECONDITION_FAILED)
            project.cancel()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class FundProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        project = Project.objects.get(id=id)
        if project:
            if project.user != user:
                return Response(status=HTTP_401_UNAUTHORIZED)
            if project.token_info.development_stage != DevelopmentStages.Inception.value:
                return Response(data={"stage error"}, status=HTTP_412_PRECONDITION_FAILED)
            project.fund()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ReleaseProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        project = Project.objects.get(id=id)
        if project:
            if project.user != user:
                return Response(status=HTTP_401_UNAUTHORIZED)
            if project.token_info.development_stage != DevelopmentStages.Elaboration.value:
                return Response(data={"stage error"}, status=HTTP_412_PRECONDITION_FAILED)
            project.release()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
