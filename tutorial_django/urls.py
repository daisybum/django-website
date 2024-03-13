from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views

urlpatterns = [
    path('', blog_views.main, name='main'),
    path('admin/', admin.site.urls, name='admin'),
    path('blog/', include('blog.urls')),
    path('', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
