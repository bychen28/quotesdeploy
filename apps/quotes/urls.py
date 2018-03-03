from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.loginpage),
	url(r'^register$', views.register),
	url(r'^logout$', views.logout),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^additem$', views.makequote),
	url(r'^add$', views.addquote),
	url(r'^wish_items/(?P<iid>\d+)$', views.showitem),
	url(r'^add/(?P<iid>\d+)$', views.addfavquote),
	url(r'^remove/(?P<iid>\d+)$', views.remove)
]