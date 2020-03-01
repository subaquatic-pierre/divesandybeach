from . models import (DiveSite, MarineLife, DiveTrip,
                      CourseLevel, CourseFAQ, Course, DiveTripInfo, CourseInfo)
from core.models import User
from django.conf import settings
from random import randint

# from django.conf import settings

# settings.configure()


def pop_db():
    entry_level = CourseLevel(title='Entry Level')
    adv_level = CourseLevel(title='Advanced Level')
    pro_level = CourseLevel(title='Pro Level')
    entry_level.save()
    adv_level.save()
    pro_level.save()

    for i in range(1, 11):
        rand_1 = randint(1, 50)
        rand_2 = randint(1, 50)
        rand_3 = randint(1, 50)
        price_1 = randint(1000, 2000)
        price_2 = randint(1000, 2000)
        lorem = 'Enim laboris aute et sunt sunt voluptate. Velit qui eu ea velit laborum cillum.'

        # Create dive site
        dive_site = DiveSite(title='Dive Site ' + str(i),
                             min_diver_level='Minimum diver level ' + str(i),
                             dive_time=rand_1, depth=rand_2,
                             info=lorem)

        # Create Marine life
        marine_life = MarineLife(name='Marine Life ' + str(i),
                                 latin_name='some Latinus Name ' + str(i),
                                 abundance='plenty of them', description=lorem,
                                 link='www.linkius-spedius.com')

        # Assign marine life to site
        marine_life.save()
        print('New marine life created')
        dive_site.save()
        # dive_site.marine_life.add(marine_life)
        # dive_site.save()

        print('New dive site created')
        print('Marine life added to dive site')

        # Create course FAQ
        faq = CourseFAQ(
            question='What Questions? ' + str(rand_2),
            answer=lorem)

        # Create course
        course = Course(title='Course ' + str(i),
                        level=adv_level,
                        description=lorem,
                        min_age=rand_1, duration='that long',
                        num_pool_dives=rand_2,
                        num_ocean_dives=rand_1,
                        qualified_to=lorem,
                        schedule=lorem)

        # Assign FAQ to course
        faq.save()
        print('New FAQ created')
        course.save()
        course.faq.add(faq)
        if i < 5:
            course.level = pro_level
        else:
            course.level = adv_level
        course.save()
        print('New course created')

        # Create dive trip
        if i < 3:
            dive_trip = DiveTrip(
                title='Dive Trip ' + str(i),
                description=lorem,
                trip_type='Boat Dive',
                schedule='SCHEDULE : ' + lorem
            )
            for f in range(1, 3):
                trip_info = DiveTripInfo(
                    heading='Dive Trip Info Heading' + str(f),
                    text=lorem * 2,
                    dive_trip=dive_trip
                )

        for f in range(1, 3):
            course_info = CourseInfo(
                title='Course Info Title' + str(f),
                heading='Course Info Heading' + str(f),
                text=lorem * 2,
            )

        # from diving.pop_db import pop_db
        # Save items
