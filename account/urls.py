from django.conf.urls import url, include

urlpatterns = [
    # Url Entries for social auth
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Url Entries for django administration
    url('', include('django.contrib.auth.urls', namespace='auth')),
]
