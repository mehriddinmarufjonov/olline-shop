from django.urls import path
from .views import ProductList, AllProductsList, SortingProductList, SortingBySubcategories, ProductDetail, rate


urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductsList.as_view(), name='all_products'),
    path('sorting/<slug:key_name>/', SortingProductList.as_view(), name='sorting'),
    path('subcategory/<slug:slug>/', SortingBySubcategories.as_view(), name='subcategory'),
    path('detail/<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('rate/<int:product_id>/<int:rating>/', rate),
]