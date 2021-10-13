from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import PIL

from .converter import convert


def home(request):
    return HttpResponse('works!')


@require_POST
@csrf_exempt
def upload_img(request):
    width = request.POST.get('width', 128)
    height = request.POST.get('height', 64)
    image = request.FILES['file']


    try:
        response = convert(image, (width, height))
        status = 200
    except PIL.UnidentifiedImageError as e:
        return JsonResponse({'error': 'Incorrect file contents (only images are allowed).'}, 
                status=422)

    return JsonResponse({'payload': response}, status=status)
