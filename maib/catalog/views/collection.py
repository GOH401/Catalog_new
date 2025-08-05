from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from maib.catalog.models import Collection
from maib.catalog.forms import CollectionForm

@login_required
def collection_list(request):
    collections = Collection.objects.all()
    return render(request, 'catalog/collection_list.html', {'collections': collections})

@login_required
def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm()
    return render(request, 'catalog/collection_form.html', {'form': form})

@login_required
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'catalog/collection_form.html', {'form': form, 'collection': collection})

@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        messages.success(request, "Коллекция успешно удалена!")
        return redirect('collection_list')
    return render(request, 'catalog/collection_confirm_delete.html', {'collection': collection})