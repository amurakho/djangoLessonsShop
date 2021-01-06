import django_filters

from product.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    order = django_filters.OrderingFilter(fields=(
        ('price', 'price'),
    ))

    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ()