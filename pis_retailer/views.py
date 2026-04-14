from django.views.generic import View
from django.http import JsonResponse

from pis_com.mixins import AuthRequiredMixin


class RetailerProductsAPI(AuthRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        retailer = self.request.user.retailer_user.retailer
        products = retailer.retailer_product.all()
        products_list = []

        for product in products:
            products_list.append({
                'product_name': product.name,
                'brand_name': product.brand_name,
                'retailer': retailer.id
            })

        return JsonResponse({'retailer_products': products_list})
