from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .converter import convert


def home(request):
    return HttpResponse('works!')


@require_POST
@csrf_exempt
def upload_img(request):
    width = request.POST.get('width', 128)
    height = request.POST.get('height', 64)
    image = request.FILES['file']
    bytelist = convert(image, (width, height))

    return JsonResponse({'payload': bytelist}, status=200)
