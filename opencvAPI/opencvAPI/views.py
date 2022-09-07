import os
from .settings import MEDIA_ROOT
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def frames(request, video):
    print('here')
    path = os.path.join(MEDIA_ROOT, 'frames/' + video)  # insert the path to your directory
    img_list = os.listdir(path)
    return Response({'images': img_list}, status=200)


@api_view(['GET', 'POST'])
def videos_to_edit(request):
    print('here')
    path = os.path.join(MEDIA_ROOT, 'original')  # insert the path to your directory
    videos_list = os.listdir(path)
    return Response({'videos': videos_list}, status=200)
