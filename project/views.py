from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from project.serializers import *
from utils.web3provider import get_provider
from wallet.tokens import mint_token


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

        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(p.user.wallet.encrypted_private_key, p.user.username)
        result = eth_p.get_sharif_starter().create_project(p.user.wallet.address, pk, eth_p.manager, p.name,
                                                           str.upper(p.token_info.symbol), "",p.token_info.total_supply)
        p.contract_address = result['logs'][0]['address']

        mint_token(p)
        p.save()
        return Response(ProjectSerializer(p).data)


class GetProjectInfo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id = int(request.data['id'])
        p = Project.objects.get(id=id)
        return Response(ProjectSerializer(p).data)


class MyProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(user=request.user)
        projects_res = []
        for p in projects:
            projects_res.append(ProjectSerializer(p).data)
        return Response(projects_res)


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


class GetSymbol(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        project = '0x02EE3ED360139B2245ac9Df3E764fe90176d392a'
        return Response(get_provider().get_project(project).functions.symbol().call())
        # return Response(status=HTTP_400_BAD_REQUEST)
