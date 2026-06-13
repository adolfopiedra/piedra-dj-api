from functools import wraps
from django.http import JsonResponse


def get_request_from_args(args):
    """
    Gets the Django request object from a function-based view
    or from a class-based view method.

    Case 1:
        def view(request):
            args[0] is request

    Case 2:
        def selectall(self):
            args[0] is self
            request is available as self.request

    Case 3:
        def insert(self, request):
            args[0] is self
            args[1] is request
            request is also available as self.request
    """

    if not args:
        return None

    first_arg = args[0]

    # Function-based view: first argument is request
    if hasattr(first_arg, "user"):
        return first_arg

    # Class-based view method: first argument is self
    if hasattr(first_arg, "request"):
        return first_arg.request

    return None


def json_permission_required(permission):
    """
    Checks if the user is authenticated and has the required permission.
    Returns JSON responses instead of Django redirects.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(*args, **kwargs):

            request = get_request_from_args(args)

            if request is None:
                return JsonResponse({
                    "ok": False,
                    "message": "Internal error. Request object was not found.",
                    "data": []
                }, status=500)

            if not request.user.is_authenticated:
                return JsonResponse({
                    "ok": False,
                    "message": "You are not authenticated",
                    "data": []
                }, status=401)

            if not request.user.has_perm(permission):
                return JsonResponse({
                    "ok": False,
                    "message": "You do not have permission to perform this operation",
                    "data": []
                }, status=403)

            return view_func(*args, **kwargs)

        return wrapper

    return decorator