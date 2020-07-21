# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect


class RetailerProductsAPI(View):
    """
    API URL for Developers => {%
        url 'retailer:retailer_products'
        retailer_id=request.user.retailer_user.retailer.id
    %}
    URL Endpoint => /retailer/1/products/
    this API returns the retailer product details in json format
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            RetailerProductsAPI, self).dispatch(request, *args, **kwargs)

    def get(self, requst, *args, **kwargs):
        retailer = self.request.user.retailer_user.retailer
        products = retailer.retailer_product.all()
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
