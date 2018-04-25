# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.http import JsonResponse


class RetailerProductsAPI(View):
    """
    API URL => {% url 'retailer:retailer_products' retailer_id=request.user.retailer_user.retailer.id %}
    """

    def get(self, requst, *args, **kwargs):
        retailer = self.request.user.retailer_user.retailer
        products = retailer.retailer_product.all()
        retailer_products = {}
        products_list = []

        for product in products:
            products_list.append({
                'product_name': product.name,
                'brand_name': product.brand_name,
                'retailer': retailer.id
            })

        return JsonResponse(
            {'retailer_products': products_list}
        )
