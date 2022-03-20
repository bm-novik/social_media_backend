from django_filters.rest_framework import (FilterSet,
                                           NumberFilter,
                                           )

from .models import Like


class LikeFilter(FilterSet):
    value = NumberFilter(lookup_expr='iexact')
    user__id = NumberFilter(lookup_expr='iexact')
    ImagePost__id = NumberFilter(lookup_expr='iexact')


    class Meta:
        model = Like
        fields = ['value', 'user__id', 'ImagePost__id']
