from django.conf.urls import url, include


from pis_com.views import HomePageView
from pis_com.views import LoginView
from pis_com.views import LogoutView
from pis_com.views import (
    CreateCustomer, CustomerTemplateView, CustomerUpdateView, CreateFeedBack)
from pis_com.views import RegisterView, ReportsView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(
        r'^api/', include('pis_com.api_urls', namespace='com_api')
    ),
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

    url(
        r'^customer/(?P<pk>\d+)/update$',
        CustomerUpdateView.as_view(),
        name='update_customer'
    ),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(
        r'^feedback/create/$',
        CreateFeedBack.as_view(),
        name='create_feedback'
    ),
]

