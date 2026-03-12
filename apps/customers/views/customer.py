from django.http import HttpResponse
def get_all(request):
    return HttpResponse("Get all customers")