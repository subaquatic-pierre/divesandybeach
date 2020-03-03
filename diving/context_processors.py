from .models import Category
from django.template import RequestContext, Context


def nav_links(request):
    return []
    # course_levels = []
    # course_levels.append(Category.objects.get(title='Entry Level'))
    # course_levels.append(Category.objects.get(title='Advanced Level'))
    # course_levels.append(Category.objects.get(title='Specialty Courses'))
    # course_levels.append(Category.objects.get(title='Professional Level'))
    # course_levels.append(Category.objects.get(title='TecRec Level'))
    # return {'nav_course_levels': course_levels}
