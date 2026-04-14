import factory
from decimal import Decimal
from django.contrib.auth.models import User

from pis_com.models import Customer, FeedBack, AdminConfiguration
from pis_retailer.models import Retailer, RetailerUser
from pis_product.models import (
    Product, StockIn, ProductDetail, PurchasedProduct,
    ExtraItems, StockOut, ClaimedProduct,
)
from pis_sales.models import SalesHistory
from pis_ledger.models import Ledger
from pis_expense.models import ExtraExpense
from pis_employees.models import Employee, EmployeeSalary
from pis_supplier.models import Supplier, SupplierStatement


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, password='testpass123', **kwargs)


class RetailerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Retailer

    name = factory.Sequence(lambda n: f'Retailer {n}')
    slug = factory.Sequence(lambda n: f'retailer-{n}')


class RetailerUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RetailerUser

    user = factory.SubFactory(UserFactory)
    retailer = factory.SubFactory(RetailerFactory)
    role_type = RetailerUser.ROLE_TYPE_OWNER


class AdminConfigurationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdminConfiguration

    production = False
    demo = False
    local = True


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    retailer = factory.SubFactory(RetailerFactory)
    customer_name = factory.Sequence(lambda n: f'Customer {n}')
    customer_phone = factory.Sequence(lambda n: f'03001234{n:03d}')
    customer_type = 'customer'


class FeedBackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedBack

    retailer = factory.SubFactory(RetailerFactory)
    description = factory.Faker('sentence')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    brand_name = factory.Sequence(lambda n: f'Brand {n}')
    retailer = factory.SubFactory(RetailerFactory)
    unit_type = Product.UNIT_TYPE_QUANTITY
    bar_code = factory.Sequence(lambda n: f'{4000000000000 + n}')


class StockInFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockIn

    product = factory.SubFactory(ProductFactory)
    quantity = Decimal('100')
    price_per_item = Decimal('50.00')
    total_amount = Decimal('5000.00')
    buying_price_item = Decimal('30.00')
    total_buying_amount = Decimal('3000.00')


class ProductDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductDetail

    product = factory.SubFactory(ProductFactory)
    retail_price = Decimal('50.00')
    consumer_price = Decimal('45.00')
    available_item = 100
    purchased_item = 0


class SalesHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesHistory

    retailer = factory.SubFactory(RetailerFactory)
    receipt_no = factory.Sequence(lambda n: f'{1000000 + n}')
    grand_total = Decimal('500.00')
    paid_amount = Decimal('500.00')
    remaining_payment = Decimal('0')
    discount = Decimal('0')
    total_quantity = Decimal('5')


class PurchasedProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchasedProduct

    product = factory.SubFactory(ProductFactory)
    invoice = factory.SubFactory(SalesHistoryFactory)
    quantity = Decimal('5')
    price = Decimal('50.00')
    purchase_amount = Decimal('250.00')


class ExtraItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExtraItems

    retailer = factory.SubFactory(RetailerFactory)
    item_name = factory.Sequence(lambda n: f'Extra Item {n}')
    quantity = Decimal('2')
    price = Decimal('100.00')
    total = Decimal('200.00')


class StockOutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockOut

    product = factory.SubFactory(ProductFactory)
    stock_out_quantity = Decimal('10')
    selling_price = Decimal('500.00')
    buying_price = Decimal('300.00')


class ClaimedProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClaimedProduct

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    claimed_items = 2
    claimed_amount = Decimal('100.00')


class LedgerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ledger

    retailer = factory.SubFactory(RetailerFactory)
    customer = factory.SubFactory(CustomerFactory)
    amount = Decimal('500.00')
    payment = Decimal('200.00')
    description = factory.Faker('sentence')


class ExtraExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExtraExpense

    amount = Decimal('500')
    description = factory.Faker('sentence')


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    name = factory.Sequence(lambda n: f'Employee {n}')
    father_name = factory.Faker('name')
    cnic = factory.Sequence(lambda n: f'12345-6789012-{n}')
    mobile = factory.Sequence(lambda n: f'03001234{n:03d}')
    address = factory.Faker('address')
    date_of_joining = '2024-01-01'


class EmployeeSalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeSalary

    employee = factory.SubFactory(EmployeeFactory)
    salary_amount = Decimal('50000')


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Sequence(lambda n: f'Supplier {n}')
    address = factory.Faker('address')
    phone = factory.Sequence(lambda n: f'021-1234{n:03d}')
    mobile_no = factory.Sequence(lambda n: f'03001234{n:03d}')


class SupplierStatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SupplierStatement

    supplier = factory.SubFactory(SupplierFactory)
    supplier_amount = Decimal('10000.00')
    payment_amount = Decimal('5000.00')
    description = factory.Faker('sentence')
