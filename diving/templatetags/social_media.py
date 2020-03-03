from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def og_image(context):
    try:
        og_image_url = f"https://scubdaidivedubai.com{context['object'].image.image.url}"
    except Exception:
        og_image_url = "https://scubadivedubai.com/static/core/img/Untitled-2_0006_IMG_5579-2.jpg"

    return og_image_url
