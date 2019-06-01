from __future__ import unicode_literals
from django.contrib import admin

from pis_retailer.models import Retailer
from pis_retailer.models import RetailerUser


class RetailerAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'slug', 'created_at', 'updated_at',
        'package', 'package_price', 'package_expiry'
    )
    search_fields = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}


class RetailerUserAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'retailer', 'employee_name', 'email', 'phone_no', 'mobile_no',)
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'user__user_profile__phone_no',
        'user__user_profile__mobile_no', 'retailer__name'
    )
    raw_id_fields = ('retailer', 'user')

    @staticmethod
    def retailer(obj):
        return obj.retailer.name

    @staticmethod
    def email(obj):
        return obj.user.email

    @staticmethod
    def phone_no(obj):
        return obj.user.user_profile.phone_no

    @staticmethod
    def employee_name(obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)

    @staticmethod
    def mobile_no(obj):
        return obj.user.user_profile.mobile_no


admin.site.register(Retailer, RetailerAdmin)
admin.site.register(RetailerUser, RetailerUserAdmin)
