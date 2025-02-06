from utils.logger import Logger
from rest_framework.response import Response
from rest_framework import status

class ResponseFactory:
    logger = Logger().get_logger()

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
    def internal_server_error(message, data=None):
        ResponseFactory.logger.error(message)
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)