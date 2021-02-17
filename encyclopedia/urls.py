from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.entries, name='entries'),
    path('search', views.search, name='search'),
    path('new', views.new, name='new'),
    path('edit/<str:title>', views.editContent, name='edit'),
    path('random', views.randomContent, name='random'),
]
