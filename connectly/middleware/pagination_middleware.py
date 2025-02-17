import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from utils.config_manager import ConfigManager
from utils.response_factory import ResponseFactory

class PaginationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.config = ConfigManager()
        self.page_size = self.config.get_settings("DEFAULT_PAGE_SIZE") or 10  # Default to 10

    def __call__(self, request):
        response = self.get_response(request)

        # Ensure response is JsonResponse
        if not isinstance(response, JsonResponse):
            return response

        try:
            response_data = json.loads(response.content.decode("utf-8"))  # Extract JSON data
        except json.JSONDecodeError:
            return response

        # Ensure response data is a list (pagination only applies to lists)
        if not isinstance(response_data, list):
            return response

        return self.paginate_response(response_data, request)

    def paginate_response(self, data, request):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return ResponseFactory.bad_request("Invalid page number", {"error": "Page number must be an integer"})

        paginator = Paginator(data, self.page_size)

        try:
            current_page = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            return ResponseFactory.bad_request("Invalid page number", {"error": "Page out of range"})

        paginated_response = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": current_page.number,
            "next": current_page.next_page_number() if current_page.has_next() else None,
            "previous": current_page.previous_page_number() if current_page.has_previous() else None,
            "results": list(current_page.object_list)  # Ensure JSON serializability
        }

        # Directly return ResponseFactory output (which is already a JsonResponse)
        return ResponseFactory.success("Results paginated successfully", paginated_response)
