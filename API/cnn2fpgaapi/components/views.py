from rest_framework import generics
from .models import Music
from .serializers import MusicSerializer
from django.http import JsonResponse
from .process.main import Processment
# Create your views here.
class MusicList(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        print(request.headers)
        custom_header_value = request.headers.get('X-Custom-Header', 'default-value')

        data = {
            "message": "Header recebido com sucesso",
            "header_value": Processment().main(custom_header_value)
        }
        return JsonResponse(data)