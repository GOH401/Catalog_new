from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from maib.catalog.models import Carpet
from maib.catalog.forms import CarpetForm

@login_required
def carpet_create(request):
    if request.method == 'POST':
        form = CarpetForm(request.POST, request.FILES)
        if form.is_valid():
            carpet = form.save()  # Сохраняем объект в переменную
            messages.success(request, 'Товар добавлен!')
            return redirect('collection_detail', pk=carpet.collection.id)
    else:
        form = CarpetForm()
    return render(request, 'catalog/catalog_form.html', {'form': form})

@login_required
def carpet_update(request, pk):
    carpet = get_object_or_404(Carpet, pk=pk)
    if request.method == 'POST':
        form = CarpetForm(request.POST, request.FILES, instance=carpet)
        if form.is_valid():
            form.save()
            return redirect('carpet_detail', pk=carpet.pk)
    else:
        form = CarpetForm(instance=carpet)
    return render(request, 'catalog/catalog_form.html', {'form': form, 'carpet': carpet})

@login_required
def carpet_delete(request, pk):
    carpet = get_object_or_404(Carpet, pk=pk)
    if request.method == 'POST':
        carpet.delete()
        messages.success(request, 'Ковер успешно удалён!')
        return redirect('collection_detail', pk=carpet.collection.id)
    return render(request, 'catalog/catalog_confirm_delete.html', {'carpet': carpet})