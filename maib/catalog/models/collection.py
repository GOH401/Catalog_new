from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=100)
    main_colors = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Основные цвета (через запятую)"
    )

    def get_main_colors_list(self):
        return [color.strip() for color in self.main_colors.split(',') if color.strip()]