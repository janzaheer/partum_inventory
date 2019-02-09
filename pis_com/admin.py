from __future__ import unicode_literals
from django.contrib import admin

from pis_com.models import UserProfile
from pis_com.models import Customer, FeedBack
from pis_com.models import AdminConfiguration


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'first_name', 'last_name', 'phone_no',
        'email', 'user_type'
    )
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'phone_no'
    )

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def email(obj):
        return obj.user.email


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'customer_phone','customer_type', 'retailer'
    )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'retailer','description','date'
    )



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FeedBack, FeedbackAdmin)
admin.site.register(AdminConfiguration)
