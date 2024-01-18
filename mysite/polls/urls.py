
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('connectivity', views.connectivity, name="connectivity"),
    path('help', views.support, name="support"),
    path('pwr', views.pwr, name="pwr"),
    path('storage', views.storage, name="storage"),
    path('thanks', views.thanks, name="thanks"),
    path('fan_on/', views.fan_on, name="fan_on"),
    path('fan_off/', views.fan_off, name="fan_off"),
    path('fan_run_for_5_minutes/', views.fan_run_for_5_minutes, name="fan_run_for_5_minutes"),

]

urlpatterns += staticfiles_urlpatterns()

