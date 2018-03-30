from django.conf.urls import url, include


from phms_com.views import HomePageView

urlpatterns = [
    url(r'^index/$', HomePageView.as_view(), name='index'),
]

