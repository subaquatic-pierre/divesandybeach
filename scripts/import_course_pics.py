from .models import Image
from django.core.files import File
import os
from django.conf import settings
from PIL import Image
import re


# from diving.import_course_pics import get_images


def get_images():
    print(os.getcwd())
    for f in os.listdir('./website_images/'):
        title = f.split('.')[0]
        path = os.path.join(
            settings.BASE_DIR, f'./website_images/{f}')
        with open(path, 'rb') as file:
            print(f'Creating {f}...')
            course_image = Image(title=title)
            course_image.image = File(file)
            course_image.save()
