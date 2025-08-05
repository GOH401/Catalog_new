import os
import io
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maib.settings")

import django
django.setup()

with io.open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "--natural-primary", "--natural-foreign", indent=2, stdout=f)