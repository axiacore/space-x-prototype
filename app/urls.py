
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import  path, include
from django.views.generic import TemplateView
from django.conf import settings
from . import views

admin_str = 'space x prototype'
admin.site.site_header = admin_str
admin.site.site_title = admin_str


urlpatterns: list = [
    path(
        '',
        views.SpaceXView.as_view(),
        name='prototype',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), path('__reload__/', include('django_browser_reload.urls'))]