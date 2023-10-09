# extrato/urls.py
from django.urls import path
from .views import ExtratoExcelView, TesteView

urlpatterns = [
    path("pdf2excel/", ExtratoExcelView.as_view(), name="extrato-excel"),
    path("teste/", TesteView.as_view(), name="teste"),
]
