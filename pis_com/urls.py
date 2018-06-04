from django.conf.urls import url, include


from pis_com.views import HomePageView
from pis_com.views import LoginView
from pis_com.views import LogoutView
from pis_com.views import CreateCustomer, CustomerTemplateView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(
        r'^customer/create/$',
        CreateCustomer.as_view(),
        name='create_customer'
    ),

url(
        r'^customers/$',
        CustomerTemplateView.as_view(),
        name='customers'
    ),
]

