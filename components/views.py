from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination

from .models import Component
from .serializers import ComponentSerializer


class RecordPagination(CursorPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    ordering = "-created"


# Create your views here.
class ComponentViewSet(ListAPIView):
    pagination_class = RecordPagination
    serializer_class = ComponentSerializer
    queryset = Component.objects \
        .select_related(
            'lifecycle_state',
            'library',
            'creator',
            'last_modifier',
            'mounting',
            'manufacturer',
            'package'
        ) \
        .prefetch_related(
            'f_nodes',
            'qualifications',
            'links',
            'reviews'
        ) \
        .annotate(total_count_links=Count("ordered_links", distinct=True)) \
        .annotate(total_count_f_nodes=Count("ordered_f_nodes", distinct=True)) \
        .annotate(total_count_qualifications=Count("annotated_qualifications", distinct=True)) \
        .annotate(total_count_reviews=Count("reviews", distinct=True))
