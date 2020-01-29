from .models import Category


def nav_links(request):
    course_levels = Category.objects.all()
    return {'nav_course_levels': course_levels}
