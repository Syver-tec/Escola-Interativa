"""
URL configuration for escola_interativa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

urlpatterns = [
    # URLs personalizadas do feedback (incluindo admin/dashboard/)
    path('', include('feedback.urls')),
    
    # Django Admin padrão (apenas para /admin/ sem subpaths)
    path('admin/', admin.site.urls),
    
    # Internacionalização
    path('i18n/', set_language, name='set_language'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
