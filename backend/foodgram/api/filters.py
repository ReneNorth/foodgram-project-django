import django_filters
from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__id')
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(field_name='is_favorited',
                                               method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart')

    def filter_is_in_shopping_cart(self, queryset, *args):
        return queryset.filter(is_in_cart__user=self.request.user,
                               )

    def filter_is_favorited(self, queryset, *args):
        return queryset.filter(is_favorited__who_favorited=self.request.user)

    class Meta:
        model = Recipe
        fields = [
                  'tags',
                  'author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  ]
