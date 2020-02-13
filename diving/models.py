from django.db import models
from core import models as core_models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from .model_utils import (create_thumbnail, image_path, thumbnail_path,
                          create_hero_image, hero_path, medium_path, create_medium_image, create_mobile_image, mobile_path)

# Learning type used for ItemPrice model
LEARNING_TYPE_CHOICES = (
    ('E-Learning', 'E-Learning'),
    ('Book-Learning', 'Book-Learning'),
)

# Info choices for course info model
COURSE_INFO_TYPE_CHOICES = (
    ('e-learning-info', 'e-learning-info'),
    ('book-learning-info', 'book-learning-info'),
    ('pool-info', 'pool-info'),
    ('ocean-info', 'ocean-info'),
)

# Choices for required certification level associated with DiveSite model
CERT_LEVEL_CHOICES = (
    ('Junior Scuba Diver', 'Junior Scuba Diver'),
    ('Open Water', 'Open Water'),
    ('Advanced Open Water', 'Advanced Open Water'),
    ('Rescue Diver', 'Rescue Diver'),
    ('Deep Specialty', 'Deep Specialty'),
)

# Dive site types used on DiveSite model
DIVE_SITE_TYPE_CHOICES = (
    ('Ship Wreck', 'Ship Wreck'),
    ('Coral Reef', 'Coral Reef'),
    ('Artificial / Reef', 'Artificial / Reef'),
)

# Dive trip choices used for DiveTrip model
DIVE_TRIP_CHOICES = (
    ('boat-dive', 'Boat Dive'),
    ('shore-dive', 'Shore Dive'),
)

# Dive trip time choices used for DiveTrip model
TRIP_TIME_CHOICES = (
    ('9am', '9am'),
    ('1:30pm', '1:30pm'),
)

# Equipment choices used for ItemPrice model
EQUIPMENT_CHOICES = (
    ('Full Kit', 'Full Kit'),
    ('Tanks and Weights', 'Tanks and Weights'),
    ('Excluding Equipment', 'Excluding Equipment'),
)


class DiveSite(models.Model):
    title = models.CharField(max_length=255)
    min_diver_level = models.CharField(
        max_length=255, choices=CERT_LEVEL_CHOICES, blank=True, null=True)
    site_type = models.CharField(
        max_length=255, choices=DIVE_SITE_TYPE_CHOICES, blank=True, null=True)
    dive_time = models.IntegerField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True,
                            blank=True, editable=False)
    marine_life = models.ManyToManyField('MarineLife', blank=True)
    map_image = models.ImageField(
        upload_to=image_path, default='map_default.jpg')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Dive Sites'

    def __str__(self):
        return f'{self.title}'


class MarineLife(models.Model):
    name = models.CharField(max_length=255)
    latin_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    abundance = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Marine Life'


class DiveTrip(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    trip_type = models.CharField(
        max_length=255, choices=DIVE_TRIP_CHOICES, blank=True, null=True)
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    schedule = models.TextField(blank=True, null=True)

    @property
    def fk_price(self):
        try:
            item = ItemPrice.objects.get(
                dive_trip_type=self.trip_type, dive_trip_equipment='FK')
            return item.price
        except ObjectDoesNotExist:
            return None

    @property
    def tw_price(self):
        try:
            item = ItemPrice.objects.get(
                dive_trip_type=self.trip_type, dive_trip_equipment='TW')
            return item.price
        except ObjectDoesNotExist:
            return None

    @property
    def no_price(self):
        try:
            item = ItemPrice.objects.get(
                dive_trip_type=self.trip_type, dive_trip_equipment='NO')
            return item.price
        except ObjectDoesNotExist:
            return None

    @property
    def trip_info(self):
        try:
            info = DiveTripInfo.objects.all()
            return info
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Dive Trips'


class DiveTripInfo(models.Model):
    heading = models.CharField(max_length=600)
    text = models.TextField()
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    dive_trip = models.ForeignKey(
        'DiveTrip', on_delete=models.CASCADE, related_name='info')

    def __str__(self):
        return f'{self.heading}'

    class Meta:
        verbose_name_plural = 'Dive Trip Info'


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=255, null=True,
                            blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def get_nav_url(self):
        return f'/padi-level/{self.slug}'

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Catagories'


class Course(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    overview_image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL, related_name='overview_image')
    info_image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL, related_name='info_image')
    description = models.TextField(blank=True, null=True)
    e_learning_link = models.CharField(max_length=255, null=True, blank=True)
    level = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, related_name='course', null=True, blank=True)
    min_age = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True,
                            blank=True, editable=False)
    pool_dives = models.BooleanField(default=False)
    ocean_dives = models.BooleanField(default=True)
    num_pool_dives = models.IntegerField(null=True, blank=True)
    num_ocean_dives = models.IntegerField(null=True, blank=True)
    minimum_certiication_level = models.CharField(
        blank=True, null=True, choices=CERT_LEVEL_CHOICES, max_length=255)
    qualified_to = models.CharField(max_length=255, null=True, blank=True)
    schedule = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def e_learning_price(self):
        item = ItemPrice.objects.get(course=self, learning_type='E-Learning')
        return item.price

    @property
    def book_learning_price(self):
        item = ItemPrice.objects.get(
            course=self, learning_type='Book-Learning')
        return item.price

    # Information regarding the course, most courses have same info which is why seperate model
    @property
    def e_learning_info(self):
        if self.e_learning_price:
            info = CourseInfo.objects.get(info_type='e-learning-info')
            return info

    @property
    def book_learning_info(self):
        if self.book_learning_price:
            info = CourseInfo.objects.get(info_type='book-learning-info')
            return info

    @property
    def pool_info(self):
        if self.pool_dives == True:
            info = CourseInfo.objects.get(info_type='pool-info')
            return info

    @property
    def ocean_info(self):
        if self.ocean_dives == True:
            info = CourseInfo.objects.get(info_type='ocean-info')
            return info

    # @property
    # def hero_image(self):
    #     return self.images.all()

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return f'{self.title}'


class CourseInfo(models.Model):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image = models.ForeignKey(
        'Images', blank=True, null=True, on_delete=models.SET_NULL)
    info_type = models.CharField(
        max_length=255, null=True, blank=True, choices=COURSE_INFO_TYPE_CHOICES)

    # def save(self, *args, **kwargs):
    #     self.image = create_medium_image(self)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Course Info'


class Images(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_path)
    thumbnail = models.ImageField(
        editable=False, upload_to=thumbnail_path, null=True)
    hero_image = models.ImageField(
        editable=False, upload_to=hero_path, null=True)
    medium_image = models.ImageField(
        editable=False, upload_to=medium_path, null=True)
    mobile_image = models.ImageField(
        editable=False, upload_to=mobile_path, null=True)
    slug = models.SlugField(
        max_length=255, allow_unicode=True, blank=True, editable=False)
    course_pic = models.BooleanField(default=False)
    dive_site_pic = models.BooleanField(default=False)
    dive_trip_pic = models.BooleanField(default=False)
    marine_life_pic = models.BooleanField(default=False)
    client_pic = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        # if self.thumbnail == None:
        self.thumbnail = create_thumbnail(self)
        # if self.hero_image == None:
        self.hero_image = create_hero_image(self)
        # if self.medium_image == None:
        self.medium_image = create_medium_image(self)
        # if self.mobile_image == None:
        self.mobile_image = create_mobile_image(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Images'


class CourseFAQ(models.Model):
    question = models.CharField(max_length=600)
    answer = models.TextField()
    courses = models.ManyToManyField(
        'Course', related_name='faq', blank=True)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name_plural = 'Course FAQ\'s'


class ClientTestimonial(models.Model):
    client_name = models.CharField(max_length=255)
    images = models.ManyToManyField('Images', blank=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name_plural = 'Course FAQ\'s'


class ItemPrice(models.Model):
    title = models.CharField(max_length=255)
    learning_type = models.CharField(
        max_length=255, null=True, blank=True, choices=LEARNING_TYPE_CHOICES)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='items')
    course = models.ForeignKey(
        'Course', null=True, blank=True, on_delete=models.SET_NULL)
    dive_trip = models.ForeignKey(
        'DiveTrip', null=True, blank=True, on_delete=models.SET_NULL)
    dive_trip_equipment = models.CharField(
        max_length=255, null=True, blank=True, choices=EQUIPMENT_CHOICES)
    trip_type = models.CharField(
        max_length=255, null=True, blank=True, choices=DIVE_TRIP_CHOICES)

    def __str__(self):
        return f'{self.title}'


class CourseBookingRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    course = models.CharField(max_length=255, blank=True, null=True)
    extra_divers = models.TextField(blank=True, null=True)
    date = models.DateField()
    message = models.TextField(null=True, blank=True)
    date_submitted = models.DateField(auto_now_add=True)
    closed = models.BooleanField(default=False)


class DiveBookingRequest(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    time = models.CharField(
        max_length=255, choices=TRIP_TIME_CHOICES, blank=True, null=True)
    date = models.DateField()
    message = models.TextField(null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)


class DiveBookingRequestDiver(models.Model):
    full_name = models.CharField(max_length=255)
    cert_level = models.CharField(
        max_length=255, choices=CERT_LEVEL_CHOICES, blank=True, null=True)
    kit_required = models.CharField(
        max_length=255, choices=EQUIPMENT_CHOICES, blank=True, null=True)
    dive_booking_query = models.ForeignKey(
        'DiveBookingRequest', on_delete=models.CASCADE, blank=True, null=True, related_name='divers')
