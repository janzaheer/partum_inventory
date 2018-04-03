from django.conf.urls import url, include


from pis_com.views import HomePageView

urlpatterns = [
    url(r'^index/$', HomePageView.as_view(), name='index'),
]

