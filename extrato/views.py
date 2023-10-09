from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from extrato.utils.extrato import Extrato
from extrato.utils.excel import Excel
from django.http import HttpResponse
from .serializer import WordSerializer
import json

class TesteView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({'message':'teste com sucesso'})

class ExtratoExcelView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        
        file = request.FILES.get('file')
        words = request.data.get('data')
        nome = request.data.get('nome')
        
        serializer = WordSerializer(data=json.loads(words), many=True)
        if serializer.is_valid():
            words = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        
        extrato, list_words, perfil = Extrato(file, words)
        
        if (len(extrato) == 0) : 
            return Response({'message':'Nenhum resultado foi encontrado'}, status=400)
        
        excel_binario = Excel(extrato, list_words, perfil)
        
        response = HttpResponse(excel_binario, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{nome.replace(".pdf",".xlsx")}"'
        
        return response
    