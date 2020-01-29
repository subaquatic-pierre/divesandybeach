from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import io
import sys


HERO_IMAGE_SIZE = (1600, 780)
THUMB_IMAGE_SIZE = (300, 300)
MOBILE_IMAGE_SIZE = (320, 640)
MEDIUM_IMAGE_SIZE = (1000, 1000)

""" 
Size refactor should not have many if statements depending on image size,
it should create object based on image size, that object should contain parameters
which dictate charateristics
eg. HeroImageClass, ThumbImageClass
These classes sshould inheret from base image class which will have base methods
and attributes

 """


def size_refactor(image_size, image_type):
    width, height = image_size
    if image_type == 'thumb':
        f_width, f_height = THUMB_IMAGE_SIZE
    elif image_type == 'hero':
        f_width, f_height = HERO_IMAGE_SIZE
    elif image_type == 'medium':
        f_width, f_height = MEDIUM_IMAGE_SIZE
    elif image_type == 'mobile':
        f_width, f_height = MOBILE_IMAGE_SIZE

    if width > height:
        f = f_width / width
        new_width, new_height = int(width * f), int(height * f)
        # If height is smaller than required height, factor is too large
        if new_height < f_height:
            # Refactor to fit minimum height
            new_f = (f_height / new_height)
            new_width, new_height = int(
                new_width * new_f), int(new_height * new_f)
        orientation = 'landscape'
    else:
        f = f_height / height
        new_width, new_height = int(width * f), int(height * f)
        # If width is smaller than required width, factor is too large
        if new_width < f_width:
            # Refactor to fit minimum width
            new_f = (f_width / new_width)
            new_width, new_height = int(
                new_width * new_f), int(new_height * new_f)

        orientation = 'portrait'
    new_size = (new_width, new_height)
    return (new_size, orientation)


def crop_image(new_image, orientation, new_size, image_type):
    if image_type == 'thumb':
        f_width, f_height = THUMB_IMAGE_SIZE
    elif image_type == 'hero':
        f_width, f_height = HERO_IMAGE_SIZE
    elif image_type == 'mobile':
        f_width, f_height = MOBILE_IMAGE_SIZE

    if orientation == 'landscape':
        start_pos = int((new_size[1] - f_height) / 2)
        end_pos = f_height + start_pos
        new_image = new_image.crop((0, start_pos, f_width, end_pos))
    elif orientation == 'portrait':
        start_pos = int((new_size[0] - f_width) / 2)
        end_pos = f_width + start_pos
        new_image = new_image.crop((start_pos, 0, end_pos, f_height))

    return new_image


def image_path(instance, filename):
    path = f'{str(instance.__class__.__name__).lower()}/'
    filename = instance.slug + '.jpg'
    return os.path.join(path, filename)


def medium_path(instance, filename):
    path = f'{str(instance.__class__.__name__).lower()}/'
    filename = instance.slug + '-1000x1000.jpg'
    return os.path.join(path, filename)


def thumbnail_path(instance, filename):
    path = f'{str(instance.__class__.__name__).lower()}/'
    filename = instance.slug + '-300x300.jpg'
    return os.path.join(path, filename)


def hero_path(instance, filename):
    path = f'{str(instance.__class__.__name__).lower()}/'
    filename = instance.slug + '-1600x780.jpg'
    return os.path.join(path, filename)


def mobile_path(instance, filename):
    path = f'{str(instance.__class__.__name__).lower()}/'
    filename = instance.slug + '-320x640.jpg'
    return os.path.join(path, filename)


def create_thumbnail(instance):
    filename = 'new-thumbnail.jpg'
    image = Image.open(instance.image.open())
    output = io.BytesIO()
    new_size, orientation = size_refactor(image.size, 'thumb')
    new_image = image.resize(new_size, Image.ANTIALIAS)
    new_image = crop_image(new_image, orientation, new_size, 'thumb')
    new_image.save(output, format='JPEG', quality=80)
    return InMemoryUploadedFile(output, 'ImageField', filename, 'image/jpeg', sys.getsizeof(output), None)


def create_mobile_image(instance):
    filename = 'new-mobile.jpg'
    image = Image.open(instance.image.open())
    output = io.BytesIO()
    new_size, orientation = size_refactor(image.size, 'mobile')
    new_image = image.resize(new_size, Image.ANTIALIAS)
    new_image = crop_image(new_image, orientation, new_size, 'mobile')
    new_image.save(output, format='JPEG', quality=80)
    return InMemoryUploadedFile(output, 'ImageField', filename, 'image/jpeg', sys.getsizeof(output), None)


def create_hero_image(instance):
    filename = 'new-hero.jpg'
    image = Image.open(instance.image.open())
    output = io.BytesIO()
    new_size, orientation = size_refactor(image.size, 'hero')
    new_image = image.resize(new_size, Image.ANTIALIAS)
    new_image = crop_image(new_image, orientation, new_size, 'hero')
    new_image.save(output, format='JPEG', quality=70)
    return InMemoryUploadedFile(output, 'ImageField', filename, 'image/jpeg', sys.getsizeof(output), None)


def create_medium_image(instance):
    filename = 'medium.jpg'
    image = Image.open(instance.image.open())
    output = io.BytesIO()
    new_size, orientation = size_refactor(image.size, 'medium')
    new_image = image.resize(new_size, Image.ANTIALIAS)
    new_image.save(output, format='JPEG', quality=80)
    return InMemoryUploadedFile(output, 'ImageField', filename, 'image/jpeg', sys.getsizeof(output), None)
