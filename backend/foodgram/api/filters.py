import django_filters

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    # print('RecipeFilter')
    author = django_filters.CharFilter(field_name='author__id')
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(field_name='is_favorited',
                                                     method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(field_name='is_in_shopping_cart',
                                                     method='filter_is_in_shopping_cart')
    
    def filter_is_in_shopping_cart(self, queryset, *args):
        # print(queryset)
        # print(*args)
        return queryset.filter(is_in_cart__user=self.request.user,
                            #    is_in_cart__recipe_in_cart=recipe
                               )
    
    def filter_is_favorited(self, queryset, *args):
        # print(queryset)
        # print(self)
        # print(*args)
        return queryset.filter(is_favorited__who_favorited=self.request.user)

# BooleanFilter’s use the API-friendly BooleanWidget, which accepts lowercase true/false.
    class Meta:
        model = Recipe
        fields = [
            # 'id', 'tags', 'author', 'ingredients',
                  'tags',
                  'author',
                  'is_favorited',
                  'is_in_shopping_cart',
                #   'is_subscribed',
                #   'name', 'text',
                #   'cooking_time', 
                  ]

    # @staticmethod
    # def filter_name_not_in(queryset, _, value):
    #     return queryset.exclude(name__in=value.split(','))
    
    # @staticmethod
    