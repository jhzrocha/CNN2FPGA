# from rest_framework import generics
# from .models import Music
# from .serializers import MusicSerializer
# from django.http import JsonResponse
# from .process.main import Processment
import os
from django.http import FileResponse

from django.shortcuts import render
# Create your views here.
# class MusicList(generics.ListCreateAPIView):

#     def get(self, request, *args, **kwargs):
#         print(request.headers)
#         custom_header_value = request.headers.get('X-Custom-Header', 'default-value')

#         data = {
#             "message": "Header recebido com sucesso",
#             "header_value": Processment().main(custom_header_value)
#         }
#         return JsonResponse(data)
    

def component(request):
    return render(request, 'front/index.html')

def createComponent(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_arquivo = os.path.join(BASE_DIR, "components", "ComponentCreator", "Output", "CNN2FPGAVHDL.vhd")
    return FileResponse(open(caminho_arquivo, "rb"), as_attachment=True, filename="CNN2FPGAVHDL.vhd")