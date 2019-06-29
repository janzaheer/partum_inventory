from django.conf.urls import url, include

from pis_product.views import ProductItemList
from pis_product.views import ProductDetailList
from pis_product.views import AddNewProduct
from pis_product.views import AddProductItems
from pis_product.views import PurchasedItems
from pis_product.views import ExtraItemsView
from pis_product.views import ClaimedProductFormView
from pis_product.views import ClaimedItemsListView
from pis_product.views import StockItemList
from pis_product.views import AddStockItems
from pis_product.views import StockOutItems
from pis_product.views import StockDetailView
from pis_product.views import StockInListView
from pis_product.views import StockOutListView
from pis_product.views import ProductUpdateView
from pis_product.views import StockInUpdateView

from pis_product.logs_view import DailyStockLogs, MonthlyStockLogs


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
    url(
        r'^items/claimed/$', ClaimedProductFormView.as_view(),
        name='claimed_items'
    ),
    url(
        r'^items/claimed/list/$', ClaimedItemsListView.as_view(),
        name='claimed_items_list'
    ),
    url(
        r'^retailer/(?P<retailer_id>\d+)/add/$',
        AddNewProduct.as_view(),
        name='add_product'
    ),
    url(r'^stock/items/list/$', StockItemList.as_view(), name='stock_items_list'),
    url(
        r'^stock/item/(?P<product_id>\d+)/add/$',
        AddStockItems.as_view(),
        name='add_stock_items'
    ),
    url(
        r'^stock/item/(?P<product_id>\d+)/out/$',
        StockOutItems.as_view(),
        name='stock_out_items'
    ),
    url(
        r'^stock/item/(?P<product_id>\d+)/detail/$',
        StockDetailView.as_view(),
        name='stock_detail'
    ),
    url(
        r'^(?P<product_id>\d+)/stock/in/$',
        StockInListView.as_view(),
        name='stockin_list'
    ),
    url(
        r'^(?P<product_id>\d+)/stock/out/$',
        StockOutListView.as_view(),
        name='stockout_list'
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        ProductUpdateView.as_view(),
        name='update_product'
    ),
    url(
        r'^(?P<pk>\d+)/stockin/update/$',
        StockInUpdateView.as_view(),
        name='update_stockin'
    ),

    # Logs
    url(
        r'^stock/logs/daily/$', DailyStockLogs.as_view(),
        name='daily_stock_logs'
    ),
    url(
        r'^stock/logs/monthly/$', MonthlyStockLogs.as_view(),
        name='monthly_stock_logs'
    ),
]
