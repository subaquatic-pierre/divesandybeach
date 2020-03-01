from django.core.files import File
from diving.models import Image
import os
from divesandybeach.settings import BASE_DIR
from PIL import UnidentifiedImageError

for file in os.listdir(os.path.join(BASE_DIR, 'final_pics_1')):
    title = file.split('.')[0]
    path = os.path.join(BASE_DIR, 'final_pics_1', file)
    with open(path, 'rb') as f:
        print('--- Opening file ---', title)
        try:
            pic = Image(title=title, image=File(f))
            pic.save()
            print('...\n--- Saved Picture ---')
        except OSError:
            print('--- Wrong format, unable to save file ---', title)
        except UnidentifiedImageError:
            print('UnidentifiedImageError', title)

# from diving import import_website_pics
