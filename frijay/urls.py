from django.conf.urls import url
from frijay import views

#These url patterns are for 'domain.com/frijay/'.
urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
]
