from django.urls import path

from .views import ComponentViewSet

urlpatterns = [
    path('components/', ComponentViewSet.as_view(), name="list")
]
