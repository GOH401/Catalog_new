from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from maib.catalog.models import Carpet, Collection
from django.core.paginator import Paginator

def carpet_list(request, pk = None):
    """Отображение колекции"""
    query = request.GET.get('q', '')
    color = request.GET.get('color', '')
    collection_id = request.GET.get('collection', '')
    style = request.GET.get('style', '')  # Новый фильтр

    collection_id = pk or request.GET.get('collection', '')
    carpets = Carpet.objects.all()

    if query:
        carpets = carpets.filter(
            Q(name__icontains=query) |
            Q(collection__name__icontains=query)
        )

    if color:
        carpets = carpets.filter(color__iexact=color)

    if collection_id:
        carpets = carpets.filter(collection_id=collection_id)

    if style:
        carpets = carpets.filter(style__iexact=style)

    # Уникальные значения для фильтров
    all_colors = Carpet.objects.order_by('color').values_list('color', flat=True).distinct()
    all_collections = Collection.objects.all()
    all_styles = Carpet.objects.order_by('style').values_list('style', flat=True).distinct()

    # Пагинация
    paginator = Paginator(carpets, 12)  # 12 ковров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'color': color,
        'collection': collection_id,
        'style': style,
        'all_colors': all_colors,
        'all_collections': all_collections,
        'all_styles': all_styles,
    }

    return render(request, 'catalog/catalog_list.html', context)

def carpet_detail(request, pk):
    carpet = get_object_or_404(Carpet, pk=pk)

    # Похожие ковры (оставляем как было)
    similar_carpets = Carpet.objects.filter(
        Q(collection=carpet.collection) |
        Q(color__iexact=carpet.color) |
        Q(name__icontains=carpet.name.split('_')[0])
    ).exclude(pk=carpet.pk).distinct()[:6]

    # Навигация по коллекции
    collection_carpets = Carpet.objects.filter(collection=carpet.collection).order_by('id')
    ids = list(collection_carpets.values_list('id', flat=True))
    current_index = ids.index(carpet.id)

    prev_id = ids[current_index - 1] if current_index > 0 else None
    next_id = ids[current_index + 1] if current_index < len(ids) - 1 else None

    context = {
        'carpet': carpet,
        'similar_carpets': similar_carpets,
        'prev_id': prev_id,
        'next_id': next_id,
    }
    return render(request, 'catalog/catalog_detail.html', context)

def collection_cards(request):
    collections = Collection.objects.all()
    return render(request, 'catalog/collection_cards.html', {'collection_cards': collections})


def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    carpets = collection.carpets.all()
    return render(request, 'catalog/catalog_list.html', {
        'collection': collection,
        'carpets': carpets
    })