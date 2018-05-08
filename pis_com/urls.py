from django.conf.urls import url, include


from pis_com.views import HomePageView
from pis_com.views import LoginView
from pis_com.views import LogoutView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(
        r'^api/', include('pis_com.api_urls', namespace='com_api')
    )
]

