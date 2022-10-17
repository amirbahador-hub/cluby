from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, JSONParser
from typing import BinaryIO


class TestCore(APIView):
    parser_classes = (FileUploadParser, )
    def get(self, request, *args, **kwargs):
        temp_result = {
            "results": {
                "title": "Hi",
            }
        }
        return Response(temp_result)
    
    def post(self, request, *args, **kwargs):
        return Response(request.data)
