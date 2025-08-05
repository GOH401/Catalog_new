from django import forms
from maib.catalog.models import Collection


class CollectionForm(forms.ModelForm):
    main_colors = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '#ffffff, #000000'}),
        label='Основные цвета (до 8, через запятую)'
    )

    class Meta:
        model = Collection
        fields = ['name', 'main_colors']

    def clean_main_colors(self):
        raw = self.cleaned_data.get('main_colors', '')
        colors = [c.strip() for c in raw.split(',') if c.strip()]
        if len(colors) > 8:
            raise forms.ValidationError("Максимум 8 цветов.")
        for color in colors:
            if not color.startswith('#') or len(color) not in [4, 7]:
                raise forms.ValidationError(f"Неверный формат цвета: {color}")
        return ', '.join(colors)
