
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .management.commands import relay
from .views import GPIOStatusConsumer

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('connectivity', views.connectivity, name="connectivity"),
    path('help', views.support, name="support"),
    path('pwr', views.pwr, name="pwr"),
    path('storage', views.storage, name="storage"),
    path('thanks', views.thanks, name="thanks"),
    path('router_uptime/', views.router_uptime, name='router_uptime'),
    path('camera_uptime/', views.camera_uptime, name='camera_uptime'),
    path('camera_on/', views.control_device, {'device_id': 'CameraOn'}, name='camera_on'),
    path('camera_off/', views.control_device, {'device_id': 'CameraOff'}, name='camera_off'),
    path('fan_on/', views.control_device, {'device_id': 'FanOn'}, name='fan_on'),
    path('fan_off/', views.control_device, {'device_id': 'FanOff'}, name='fan_off'),
    path('fan_5min/', views.control_device, {'device_id': 'Fan5Min'}, name='fan_5min'),
    path('strobe_on/', views.control_device, {'device_id': 'StrobeOn'}, name='strobe_on'),
    path('strobe_off/', views.control_device, {'device_id': 'StrobeOff'}, name='strobe_off'),
    path('strobe_5min/', views.control_device, {'device_id': 'Strobe5Min'}, name='strobe_5min'),
    path('router_reset/', views.control_device, {'device_id': 'RouterReset'}, name='router_reset'),
    path('gpio_status/', views.gpio_status, name='gpio_status'),
]


urlpatterns += staticfiles_urlpatterns()

websocket_urlpatterns = [
    re_path(r'^ws/gpio/status/$', GPIOStatusConsumer.as_asgi()),
]