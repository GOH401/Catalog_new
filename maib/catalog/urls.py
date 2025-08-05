from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.collection_cards, name='collection_cards'),
    path('carpet/<int:pk>/', views.carpet_detail, name='carpet_detail'),
    path('carpet/add/', views.carpet_create, name='carpet_create'),
    path('carpet/<int:pk>/edit/', views.carpet_update, name='carpet_update'),
    path('carpet/<int:pk>/delete/', views.carpet_delete, name='carpet_delete'),
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/add/', views.collection_create, name='collection_create'),
    path('collections/<int:pk>/edit/', views.collection_update, name='collection_update'),
    path('collections/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    path('collection/<int:pk>/', views.carpet_list, name='collection_detail'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('collection_cards')), name='logout'),
]