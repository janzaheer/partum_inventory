import pytest
from decimal import Decimal
from django.urls import reverse

from pis_product.models import Product
from pis_product.forms import ProductForm, StockDetailsForm
from tests.factories import (
    RetailerUserFactory, RetailerFactory, ProductFactory, StockInFactory,
    ProductDetailFactory, PurchasedProductFactory, ExtraItemsFactory,
    StockOutFactory, ClaimedProductFactory, CustomerFactory, SalesHistoryFactory,
)

pytestmark = pytest.mark.django_db


class TestProductModel:
    def test_create(self):
        product = ProductFactory()
        assert product.pk is not None
        assert 'Product' in product.name

    def test_str(self):
        product = ProductFactory(name='Test Widget')
        assert str(product) == 'Test Widget'

    def test_unit_type_choices(self):
        assert Product.UNIT_TYPE_KG == 'Kilogram'
        assert Product.UNIT_TYPE_GRAM == 'Gram'
        assert Product.UNIT_TYPE_LITRE == 'Litre'
        assert Product.UNIT_TYPE_QUANTITY == 'Quantity'

    def test_total_items(self):
        product = ProductFactory()
        StockInFactory(product=product, quantity=Decimal('50'))
        StockInFactory(product=product, quantity=Decimal('30'))
        assert product.total_items() == Decimal('80')

    def test_total_items_with_no_stock(self):
        product = ProductFactory()
        assert product.total_items() == 0

    def test_available_items(self):
        product = ProductFactory()
        StockInFactory(product=product, quantity=Decimal('100'))
        invoice = SalesHistoryFactory(retailer=product.retailer)
        StockOutFactory(product=product, invoice=invoice, stock_out_quantity=Decimal('30'))
        assert product.product_available_items() == Decimal('70')

    def test_purchased_items(self):
        product = ProductFactory()
        invoice = SalesHistoryFactory(retailer=product.retailer)
        StockOutFactory(product=product, invoice=invoice, stock_out_quantity=Decimal('25'))
        assert product.product_purchased_items() == Decimal('25')

    def test_claimed_items(self):
        product = ProductFactory()
        customer = CustomerFactory(retailer=product.retailer)
        ClaimedProductFactory(product=product, customer=customer, claimed_items=3)
        ClaimedProductFactory(product=product, customer=customer, claimed_items=2)
        assert product.total_num_of_claimed_items() == 5


class TestStockInModel:
    def test_create(self):
        stock = StockInFactory()
        assert stock.pk is not None

    def test_str(self):
        product = ProductFactory(name='Widget A')
        stock = StockInFactory(product=product)
        assert str(stock) == 'Widget A'


class TestProductDetailModel:
    def test_create(self):
        detail = ProductDetailFactory()
        assert detail.pk is not None
        assert detail.available_item == 100

    def test_str(self):
        product = ProductFactory(name='Detail Product')
        detail = ProductDetailFactory(product=product)
        assert str(detail) == 'Detail Product'


class TestPurchasedProductModel:
    def test_create(self):
        purchased = PurchasedProductFactory()
        assert purchased.pk is not None
        assert purchased.quantity == Decimal('5')

    def test_str(self):
        product = ProductFactory(name='Purchased Widget')
        purchased = PurchasedProductFactory(product=product)
        assert str(purchased) == 'Purchased Widget'


class TestExtraItemsModel:
    def test_create(self):
        extra = ExtraItemsFactory()
        assert extra.pk is not None

    def test_str(self):
        extra = ExtraItemsFactory(item_name='Cable')
        assert str(extra) == 'Cable'

    def test_str_with_none(self):
        extra = ExtraItemsFactory(item_name=None)
        assert str(extra) == ''


class TestStockOutModel:
    def test_create(self):
        stock_out = StockOutFactory()
        assert stock_out.pk is not None

    def test_str(self):
        product = ProductFactory(name='Out Product')
        stock_out = StockOutFactory(product=product)
        assert str(stock_out) == 'Out Product'


class TestClaimedProductModel:
    def test_create(self):
        claimed = ClaimedProductFactory()
        assert claimed.pk is not None
        assert claimed.claimed_items == 2

    def test_str(self):
        product = ProductFactory(name='Claimed Widget')
        claimed = ClaimedProductFactory(product=product)
        assert str(claimed) == 'Claimed Widget'


class TestProductForm:
    def test_valid(self):
        retailer = RetailerFactory()
        form = ProductForm(data={
            'name': 'Test Product Form',
            'retailer': retailer.id,
            'unit_type': Product.UNIT_TYPE_QUANTITY,
        })
        assert form.is_valid()

    def test_invalid_missing_name(self):
        retailer = RetailerFactory()
        form = ProductForm(data={'retailer': retailer.id})
        assert not form.is_valid()


class TestStockDetailsForm:
    def test_valid(self):
        product = ProductFactory()
        form = StockDetailsForm(data={
            'product': product.id,
            'quantity': '50',
            'price_per_item': 100.00,
            'total_amount': 5000.00,
            'buying_price_item': 80.00,
            'total_buying_amount': 4000.00,
        })
        assert form.is_valid()


class TestProductViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_stock_items_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        ProductFactory(retailer=self.retailer_user.retailer)
        response = client.get(reverse('product:stock_items_list'))
        assert response.status_code == 200

    def test_items_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:items_list'))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('product:stock_items_list'))
        assert response.status_code == 302

    def test_stock_detail(self, client):
        client.login(username=self.user.username, password='testpass123')
        product = ProductFactory(retailer=self.retailer_user.retailer)
        StockInFactory(product=product, quantity=Decimal('50'))
        response = client.get(
            reverse('product:stock_detail', kwargs={'product_id': product.pk}))
        assert response.status_code == 200

    def test_purchased_items(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:purchased_items'))
        assert response.status_code == 200

    def test_extra_items(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:purchased_extra_items'))
        assert response.status_code == 200

    def test_claimed_items(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:claimed_items'))
        assert response.status_code == 200

    def test_stockin_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        product = ProductFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('product:stockin_list', kwargs={'product_id': product.pk}))
        assert response.status_code == 200

    def test_stockout_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        product = ProductFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('product:stockout_list', kwargs={'product_id': product.pk}))
        assert response.status_code == 200

    def test_daily_stock_logs(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:daily_stock_logs'))
        assert response.status_code == 200

    def test_monthly_stock_logs(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('product:monthly_stock_logs'))
        assert response.status_code == 200
