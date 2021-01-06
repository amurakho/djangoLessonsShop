from django.urls import path
from django.views.generic import TemplateView

from product.views import ProductListView, ProductDetailView, to_bucket, some_view, subscribe_view


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('download-pdf/', some_view),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('to-bucket/', to_bucket, name='to_bucket'),
    path('bucket/', TemplateView.as_view(template_name='bucket.html'), name='bucket_view'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
]
