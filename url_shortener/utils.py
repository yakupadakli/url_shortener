from django.template.defaultfilters import slugify


def create_unique_slug(instance, slug, _next=0):
    slug = slugify(slug if _next == 0 else "%s_%s" % (slug, _next))
    if instance.__class__.objects.filter(slug=slug).exists():
        return create_unique_slug(instance, slug, _next=_next+1)
    return slug
