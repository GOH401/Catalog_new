from django import forms

PERCENT_CHOICES = [('', '-')] + [(f"{i}%", f"{i}%") for i in range(0, 101, 5)]
MATERIAL_CHOICES = [
    ('', '— Материал —'),
    ('POLYESTER', 'POLYESTER'),
    ('AKRIL', 'AKRIL'),
    ('BCF', 'BCF'),
    ('Popip Heat Set', 'Popip Heat Set'),
]
NOTE_CHOICES = [('', '-'), ('PP', 'PP')]


class ThreadTypeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(choices=PERCENT_CHOICES),
            forms.Select(choices=MATERIAL_CHOICES),
            forms.Select(choices=PERCENT_CHOICES),
            forms.Select(choices=NOTE_CHOICES),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            parts = value.split(';')
            return parts + [''] * (4 - len(parts))
        return [''] * 4


class ThreadTypeField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [
            forms.ChoiceField(choices=PERCENT_CHOICES),
            forms.ChoiceField(choices=MATERIAL_CHOICES),
            forms.ChoiceField(choices=PERCENT_CHOICES),
            forms.ChoiceField(choices=NOTE_CHOICES),
        ]
        super().__init__(fields=fields, widget=ThreadTypeWidget(), *args, **kwargs)

    def compress(self, data_list):
        return ';'.join(data_list) if data_list else ''
