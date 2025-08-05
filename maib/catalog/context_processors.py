from maib.catalog.models import Carpet, Collection

def collections_list(request):
    return {'header_collections': Collection.objects.all()}