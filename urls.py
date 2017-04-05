from django.conf import settings
from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from routers import router

admin.site.site_header = 'Captain Administration'
admin.site.site_title = 'Captain Administration'
admin.site.index_title = 'Captain Administration'

schema_view = get_schema_view(title='Captain API')

urlpatterns = [
    url('^$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
