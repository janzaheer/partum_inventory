from django.conf.urls import url, include

from pis_product.views import ProductItemList
from pis_product.views import ProductDetailList
from pis_product.views import AddNewProduct
from pis_product.views import AddProductItems
from pis_product.views import PurchasedItems
from pis_product.views import ExtraItemsView


urlpatterns = [
    url(r'^items/list/$', ProductItemList.as_view(), name='items_list'),
    url(
        r'^item/(?P<pk>\d+)/detail/list/$',
        ProductDetailList.as_view(),
        name='item_details'
    ),
    url(
        r'^retailer/(?P<retailer_id>\d+)/add/$',
        AddNewProduct.as_view(),
        name='add_product'
    ),
    url(
        r'^item/(?P<product_id>\d+)/add/$',
        AddProductItems.as_view(),
        name='add_product_items'
    ),
    url(
        r'^items/purchased/$', PurchasedItems.as_view(),
        name='purchased_items'
    ),
    url(
        r'^items/extra/purchased/$', ExtraItemsView.as_view(),
        name='purchased_extra_items'
    ),
]