# from rest_framework import generics
# from .models import Music
# from .serializers import MusicSerializer
# from django.http import JsonResponse
# from .process.main import Processment
import json
import os
from django.http import FileResponse
import zipfile
from io import BytesIO
from django.shortcuts import render

def component(request):
    return render(request, 'front/index.html')

def createComponent(request):
    print(json.loads(request.body)) #parâmetros do frontend
  
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
        for root, dirs, files in os.walk(os.path.join(base_dir, "components", "ComponentCreator", "Output")):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, os.path.join(base_dir, "components", "ComponentCreator", "Output")))

    zip_buffer.seek(0)
    response = FileResponse(zip_buffer, as_attachment=True, filename="OutputFiles.zip")
    print(response)
    return response
    
