
from django.db import models
from maib.catalog.models import Carpet

class Batch(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    arrival_date = models.DateField(verbose_name="Дата поступления")
    status = models.CharField(max_length=50, choices=[
        ('created', 'Создана'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлено')
    ], default='created', verbose_name="Статус")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    storage_location = models.CharField(max_length=100, blank=True, verbose_name="Место хранения (склад)")
    destination = models.CharField(max_length=120, blank=True, verbose_name="Пункт назначения (куда отправляется)")

    def __str__(self):
        return f"Партия #{self.id} от {self.arrival_date}"

class BatchItem(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='items')
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество ковров")

    def __str__(self):
        return f"{self.carpet.name} x {self.quantity}"
