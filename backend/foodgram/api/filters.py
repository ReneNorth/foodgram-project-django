import logging

import django_filters
from recipe.models import Recipe

log = logging.getLogger(__name__)


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author__id', method='filter_author')
    tags = django_filters.filters.AllValuesMultipleFilter(
        field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(field_name='is_favorited',
                                               method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart')

    def filter_author(self, queryset, *args):
        user = self.request.query_params.get('author')
        if user == 'me':
            return queryset.filter(author=self.request.user)
        return queryset.filter(author_id=user)

    def filter_is_in_shopping_cart(self, queryset, *args):
        if self.request.user.is_anonymous is False:
            return queryset.filter(is_in_cart__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, *args):
        return queryset.filter(is_favorited__who_favorited=self.request.user)

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart', ]
