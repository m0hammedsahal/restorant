import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse


def allow_manager(function):
    def wrapper(request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_manager:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized Access",
                    "message": "You can't perform this action."
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponseRedirect(reverse("manager:unauthorized_access"))
        return function(request, *args, **kwargs)
    return wrapper
