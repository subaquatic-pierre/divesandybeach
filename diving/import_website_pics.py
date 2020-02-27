from django.core.files import File
from .models import Images
import os
from divesandybeach.settings import BASE_DIR
from PIL import UnidentifiedImageError

for file in os.listdir(os.path.join(BASE_DIR, 'website_images')):
    title = file.split('.')[0]
    path = os.path.join(BASE_DIR, 'website_images', file)
    with open(path, 'rb') as f:
        print('--- Opening file ---', title)
        try:
            pic = Images(title=title, image=File(f))
            pic.save()
            print('...\n--- Saved Picture ---')
        except OSError:
            print('--- Wrong format, unable to save file ---', title)
        except UnidentifiedImageError:
            print('UnidentifiedImageError', title)

# from diving import import_website_pics
