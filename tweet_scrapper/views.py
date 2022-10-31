from django.shortcuts import redirect

def redirect_to_app(request):
    response = redirect("/tweets")
    return response