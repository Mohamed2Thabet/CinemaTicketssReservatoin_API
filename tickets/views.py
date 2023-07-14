from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse

def no_rest_on_models(request):
    Guests = [
        {
            'id': 1,
            'name': 'Mohamed',
            'age': 20,
        },
        {
            'id': 2,  # Updated ID to be unique
            'name': 'Ahemd',
            'age': 18,
        },
        {
            'id': 3,
            'name': 'Salah',
            'age': 15,
        }
    ]
    return JsonResponse(Guests, safe=False)

