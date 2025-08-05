from django import forms
from maib.catalog.models import Carpet
from maib.catalog.forms.widgets import ThreadTypeField


PILE_HEIGHT_CHOICES = [('', '— Высота ворса —')] + [(f"{i} мм", f"{i} мм") for i in [4,6,8,10,12,15,20]]
DENSITY_CHOICES = [('', '— Плотность —')] + [(d, d) for d in [
    '180 000 точек/м²', '200 000 точек/м²', '224 000 точек/м²',
    '300 000 точек/м²', '400 000 точек/м²', '500 000 точек/м²'
]]
LOOM_WIDTH_CHOICES = [('', '— Ширина станка —'), ('4 м', '4 м'), ('5 м', '5 м')]


class CarpetForm(forms.ModelForm):
    pile_height = forms.ChoiceField(choices=PILE_HEIGHT_CHOICES, required=False, label="Высота ворса", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    density = forms.ChoiceField(choices=DENSITY_CHOICES, required=False, label="Плотность", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    loom_width = forms.ChoiceField(choices=LOOM_WIDTH_CHOICES, required=False, label="Ширина станка", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    yarn = forms.CharField(required=False, label="Пряжа", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))
    quality = forms.CharField(required=False, label="Качество", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))
    weight = forms.CharField(required=False, label=" кг/м²", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))

    thread_type = ThreadTypeField(required=False, label="Состав")

    class Meta:
        model = Carpet
        fields = [
            'collection', 'name', 'code', 'color', 'image', 'style',
            'loom_width', 'yarn', 'quality', 'pile_height', 'density',
            'weight', 'thread_type'
        ]
        widgets = {
            'collection': forms.Select(attrs={'class': 'carpet-form-select'}),
            'name': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'code': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'color': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'carpet-form-input'}),
            'style': forms.Select(attrs={'class': 'carpet-form-select'}),
        }
