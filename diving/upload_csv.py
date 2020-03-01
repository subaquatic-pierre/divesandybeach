from .models import ItemPrice, Category, Course, Image, DiveSite
from django.core.exceptions import ObjectDoesNotExist
import csv
import io


class UploadCSV:
    def upload(self, file):
        data_set = file.read().decode('utf-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        reader = csv.reader(io_string, delimiter=',', quotechar="|")
        return reader


class UploadItemPrice(UploadCSV):
    def upload(self, file):
        reader = super().upload(file)
        for line in reader:
            # Get info from csv sheet
            title = line[0]
            category = line[4]
            learning_type = line[2]
            trip_type = line[3]
            equipment_type = line[1]
            price = line[5]
            # Get or create items in DB
            item, created = ItemPrice.objects.get_or_create(title=title)
            category, created = Category.objects.get_or_create(title=category)
            if equipment_type:
                item.dive_trip_equipment = equipment_type
            if learning_type:
                item.learning_type = learning_type
            if trip_type:
                item.trip_type = trip_type
            item.price = price
            item.category = category

            item.save()
            print(f'Saving new item {item.title}...')

        return 1


class UploadCoursesCSV(UploadCSV):
    def upload(self, file):
        reader = super().upload(file)
        for line in reader:
            title = line[0]
            level = line[1]
            min_age = line[2]
            duration = line[3]
            num_pool_dives = line[4]
            num_ocean_dives = line[5]
            minimum_certiication_level = line[6]
            qualified_to = line[7]
            schedule = line[8]
            description = line[9]
            # Num of dives is empty
            if not num_pool_dives:
                num_pool_dives = 0
            if not num_ocean_dives:
                num_ocean_dives = 0

            level, created = Category.objects.get_or_create(title=level)
            if created:
                print(f'Creating new course level {level.title}')
            course = Course(title=title, level=level,
                            min_age=min_age, duration=duration, num_pool_dives=num_pool_dives,
                            num_ocean_dives=num_ocean_dives, minimum_certiication_level=minimum_certiication_level,
                            qualified_to=qualified_to, schedule=schedule, description=description)
            try:
                image = Image.objects.filter(title=course.title).first()
                course.image = image
            except ObjectDoesNotExist:
                print('Couldnt find image with matching name', course.title)
                pass

            print(f'Saving new course {course.title}...')
            course.save()

        return 1


class UploadDiveSitesCSV(UploadCSV):
    def upload(self, file):
        reader = super().upload(file)
        for line in reader:
            title = line[0]
            min_diver_level = line[1]
            site_type = line[2]
            dive_time = line[3]
            distance = line[4]
            depth = line[5]
            info = line[6]

            dive_site = DiveSite(title=title, min_diver_level=min_diver_level, site_type=site_type,
                                 dive_time=dive_time, distance=distance, depth=depth, info=info)

            map_image = Image.objects.filter(title=title).first()
            dive_site.map_image = map_image
            print(f'Creating dive site {dive_site}...')
            dive_site.save()

        return 1
