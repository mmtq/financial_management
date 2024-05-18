from . import models
def user_info(request):
    if request.user.is_authenticated:
        return {
            'user_name': request.user.username,   
        }
    return {}
