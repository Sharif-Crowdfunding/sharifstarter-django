from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from project.serializers import *
from utils.web3provider import get_provider
from wallet.models import TokenAsset
from wallet.tokens import mint_token


# Create your views here.
class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        shareholders = request.data['shareholders']
        data.pop('shareholders')
        print(data)
        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        basic_info_serializer = ProjectBasicInfoSerializer(data=data['basic_info'])
        basic_info_serializer.is_valid(raise_exception=True)

        token_info_serializer = ProjectTokenInfoSerializer(data=data['token_info'])
        token_info_serializer.is_valid(raise_exception=True)

        basic_info = basic_info_serializer.save()
        token_info = token_info_serializer.save()

        p = Project(user=request.user, name=serializer.validated_data['name'], image=serializer.validated_data['image'],
                    basic_info=basic_info, token_info=token_info)
        print(p)
        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(p.user.wallet.encrypted_private_key, p.user.username)
        result = eth_p.get_sharif_starter().create_project(p.user.wallet.address, pk, eth_p.manager, p.name,
                                                           str.upper(p.token_info.symbol), "",
                                                           p.token_info.total_supply)
        p.contract_address = result['logs'][0]['address']

        mint_token(p)
        p.save()

        #TODO
        # set_shareholders(p, shareholders)

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


class GetProjectShareHolders(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        project = Project.objects.get(id=id)
        shareholders = TokenAsset.objects.filter(symbol=project.token_info.symbol)
        s_list = [{'wallet_address': s.wallet.address, 'balance': s.balance} for s in shareholders]
        return Response(data=s_list, status=HTTP_200_OK)


class GetSymbol(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        project = '0x02EE3ED360139B2245ac9Df3E764fe90176d392a'
        return Response(get_provider().get_project(project).functions.symbol().call())
        # return Response(status=HTTP_400_BAD_REQUEST)


class TransferToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        sender = request.user
        if not data['symbol'] or not data['username'] or not data['token_num']:
            return Response(status=HTTP_400_BAD_REQUEST)
        project = Project.objects.get(token_info__symbol=data['symbol'])
        receiver = User.objects.get(username=data['username'])
        asset = TokenAsset.objects.get(wallet=sender.wallet, symbol=project.symbol)

        if not receiver and not asset:
            return Response(status=HTTP_412_PRECONDITION_FAILED)

        if asset.balance < int(data['token_num']):
            return Response(status=HTTP_412_PRECONDITION_FAILED)
        eth_p = get_eth_provider()
        pk = eth_p.calc_private_key(sender.wallet.encrypted_private_key, sender.username)
        result = eth_p.get_project(project.contract_address).transfer(sender.wallet.address, pk,
                                                                      receiver.wallet.address, int(data['token_num']))
        print(result)

        transfer_asset(sender.wallet, receiver.wallet, int(data['token_num']), asset.symbol)
        return Response(status=HTTP_200_OK)


def transfer_asset(s_wallet, r_wallet, amount, symbol):
    s_asset = TokenAsset.objects.get(wallet=s_wallet, symbol=symbol)
    s_asset.balance = s_asset.balance - amount
    s_asset.save()

    r_asset = TokenAsset.objects.get(wallet=r_wallet, symbol=symbol)
    if not r_asset:
        r_asset = TokenAsset(wallet=r_wallet, contract_address=s_asset.contract_address, balance=amount,
                             symbol=s_asset.symbol)
    else:
        r_asset.balance = r_asset.balance + amount
    r_asset.save()


def set_shareholders(project, shareholders):
    eth_p = get_eth_provider()
    p = eth_p.get_project(project.contract_address)
    asset = TokenAsset.objects.get(wallet=p.user.wallet)
    for s in shareholders:
        requested_share = s.token_num
        to_user = User.objects.get(username=s.username)
        if asset.balance > requested_share and to_user:
            pk = eth_p.calc_private_key(project.user.wallet.encrypted_private_key, project.user.username)
            result = p.transfer(asset.wallet.address, pk, to_user.wallet.address, requested_share)
            print(result)

            # update token asset
            transfer_asset(asset.wallet, to_user.wallet, requested_share, asset.symbol)
