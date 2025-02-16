from django.http import JsonResponse
from utils.logger import Logger
from rest_framework.response import Response
from rest_framework import status

class ResponseFactory:
    logger = Logger().get_logger()
    
    # This fixes the issue of trying to access response content before it is rendered
    @staticmethod
    def _create_rendered_response(message, data, status_code):
        ResponseFactory.logger.info(message)
        response_data = {"detail": message} if data is None else data
        return JsonResponse(data=response_data, status=status_code, safe=False)

    @staticmethod
    def success(message, data=None):
        ResponseFactory.logger.info(message)
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def created(message, data=None):
        ResponseFactory.logger.info(message)
        return Response(data, status=status.HTTP_201_CREATED)

    @staticmethod
    def deleted(message, data=None):
        ResponseFactory.logger.info(message)
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def bad_request(message, data=None):
        ResponseFactory.logger.error(message)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def not_found(message, data=None):
        ResponseFactory.logger.error(message)
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def conflict(message, data=None):
        ResponseFactory.logger.info(message)
        return Response(data, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def internal_server_error(message, data=None):
        ResponseFactory.logger.error(message)
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def too_many_requests(message, data=None):
        ResponseFactory.logger.error(message)
        return ResponseFactory._create_rendered_response(message, data, status.HTTP_429_TOO_MANY_REQUESTS)