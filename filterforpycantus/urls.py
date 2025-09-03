"""
URL configuration for filterforpycantus project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/filter')),
    path('admin/', admin.site.urls),
    path('filter/', include('filter.urls')),
]
