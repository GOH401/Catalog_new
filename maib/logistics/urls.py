from django.urls import path
from . import views
from .views import export_batch_detail_xlsx, batch_report

urlpatterns = [
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/create/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('logistics/batches/<int:pk>/delete/', views.batch_delete, name='batch_delete'),
    path('logistics/batches/<int:pk>/export/', export_batch_detail_xlsx, name='export_batch_detail_xlsx'),
    path('logistics/batches/report/', batch_report, name='batch_report')
]