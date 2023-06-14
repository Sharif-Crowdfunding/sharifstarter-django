from django.urls import path, include

from project.views import *

urlpatterns = [
    path('create/', CreateProjectView.as_view()),
    path('my/', MyProjects.as_view()),
    path('info/', GetProjectInfo.as_view()),
    path('cancel/<id>/', CancelProject.as_view()),
    path('fund/<id>/', FundProject.as_view()),
    path('release/<id>/', ReleaseProject.as_view()),
    path('symbol/<id>/', GetSymbol.as_view()),
    path('transfer/', TransferToken.as_view()),
    path('shareholders/<id>/', GetProjectShareHolders.as_view()),
]
