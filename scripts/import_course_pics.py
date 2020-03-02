from diving.models import Image
from diving.models import Course
from django.core.files import File
import os
from django.conf import settings
from PIL import Image
import re
import sys


# from diving.import_course_pics import get_images
courses = Course.objects.all()
for course in courses:
    # print('Editing course', course)

    for i in range(1, 5):
        image_fn = os.path.join('final_website_pic_2',
                                f'PADI {course.title} {i}.jpg')

        try:
            with open(image_fn, 'rb') as f:
                pass
                # print('Opening image', f)
                # print(f)
                # print('Almost saving image')
        except FileNotFoundError:
            print('File not found:\n', image_fn)


# def get_images():
#     print(os.getcwd())
#     for f in os.listdir('./website_images/'):
#         title = f.split('.')[0]
#         path = os.path.join(
#             settings.BASE_DIR, f'./website_images/{f}')
#         with open(path, 'rb') as file:
#             print(f'Creating {f}...')
#             course_image = Image(title=title)
#             course_image.image = File(file)
#             course_image.save()


# from scripts import import_course_pics
