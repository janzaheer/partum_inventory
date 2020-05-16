"""partum_inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'^', include('pis_com.urls')),
    re_path(r'^product/', include(('pis_product.urls', 'product'),namespace='product'),),
    re_path(r'^retailer/', include(('pis_retailer.urls', 'retailer'), namespace='retailer')),
    re_path(r'^sales/', include(('pis_sales.urls', 'sales'), namespace='sales')),
    re_path(r'^ledger/', include(('pis_ledger.urls','ledger'), namespace='ledger')),
    re_path(r'^expense/', include(('pis_expense.urls','expense'), namespace='expense')),
    re_path(r'^employee/', include(('pis_employees.urls','employee'), namespace='employee')),
    re_path(r'^supplier/', include(('pis_supplier.urls','supplier'), namespace='supplier')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)