from django.urls import path, include


from pis_com.views import HomePageView
from pis_com.views import LoginView
from pis_com.views import LogoutView
from pis_com.views import (
    CreateCustomer, CustomerTemplateView, CustomerUpdateView, CreateFeedBack)
from pis_com.views import RegisterView, ReportsView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    #path('api/', include('pis_com.api_urls', namespace='com_api')),
    path('customer/create/$',CreateCustomer.as_view(),name='create_customer'),

    path('customers/$', CustomerTemplateView.as_view(), name='customers'),

    path('customer/(?P<pk>\d+)/update$', CustomerUpdateView.as_view(), name='update_customer'),
    path('register/$', RegisterView.as_view(), name='register'),
    path('feedback/create/$', CreateFeedBack.as_view(), name='create_feedback'),
]
