from django.conf.urls import url

from . import views

print "reached core urls.py"

urlpatterns = [
    # url(r'^$', views.index),
    url(r'^$', views.login_view),
    url(r'^login', views.login_view),
    # url(r'^logout', views.logout_view),
    # url(r'^register', views.register_profile),
    # url(r'^update_profile/', views.update_profile),
    # url(r'^$', views.user_profile),
    # url(r'^login$', views.login),
    # url(r'^new$', views.register),
    # url(r'^(?P<item_number>[0-9]+)/$', views.show),
    # url(r'^(?P<item_number>[0-9]+)/$', views.get_number),
    # url(r'^(?P<item_number>[0-9]+)/(edit)$', views.edit),
    # url(r'^(?P<item_number>[0-9]+)/(delete)$', views.delete),
    # url(r'^(P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views_month_archive),
]
