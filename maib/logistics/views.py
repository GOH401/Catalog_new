from django.shortcuts import render, redirect, get_object_or_404
from .models import Batch
from .forms import BatchForm, BatchItemForm, BatchItemFormSet
from django.contrib import messages
import openpyxl
from django.http import HttpResponse
import json


def batch_list(request):
    batches = Batch.objects.all().order_by('-created_at')
    return render(request, 'logistics/batch_list.html', {'batches': batches})


def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        formset = BatchItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            batch = form.save()
            formset.instance = batch
            formset.save()
            return redirect('batch_list')
    else:
        form = BatchForm()
        formset = BatchItemFormSet()
    return render(request, 'logistics/batch_form.html', {'form': form, 'formset': formset})

def batch_detail(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    carpets = batch.items.select_related('carpet')


    stats = {}
    for item in carpets:
        name = item.carpet.name
        stats[name] = stats.get(name, 0) + item.quantity


    chart_labels = list(stats.keys())
    chart_data = list(stats.values())

    return render(
        request,
        'logistics/batch_detail.html',
        {
            'batch': batch,
            'chart_labels': json.dumps(chart_labels, ensure_ascii=False),
            'chart_data': json.dumps(chart_data),
        }
    )

def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        messages.success(request, f"Партия #{pk} удалена.")
        return redirect('batch_list')
    return redirect('batch_list')


def batch_update(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        formset = BatchItemFormSet(request.POST, instance=batch)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)
        formset = BatchItemFormSet(instance=batch)
    return render(request, 'logistics/batch_form.html', {'form': form, 'formset': formset, 'batch': batch})

def batch_report(request):
    # Создаём книгу и лист
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Партии ковров"
    # Заголовки
    ws.append(['ID партии', 'Дата поступления', 'Статус', 'Ковер', 'Количество'])

    # Данные по всем партиям
    for batch in Batch.objects.prefetch_related('items__carpet'):
        items = batch.items.all()
        if items:
            for item in items:
                ws.append([
                    batch.id,
                    batch.arrival_date.strftime("%d.%m.%Y") if batch.arrival_date else '',
                    batch.get_status_display(),
                    item.carpet.name if item.carpet else '',
                    item.quantity
                ])
        else:
            ws.append([
                batch.id,
                batch.arrival_date.strftime("%d.%m.%Y") if batch.arrival_date else '',
                batch.get_status_display(),
                '',
                ''
            ])

    # Генерация файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="batches_report.xlsx"'
    wb.save(response)
    return response

def export_batch_detail_xlsx(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Партия {batch.id}"
    ws.append(['Ковер', 'Количество'])
    for item in batch.items.all():
        ws.append([item.carpet.name if item.carpet else '', item.quantity])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="batch_{batch.id}_report.xlsx"'
    wb.save(response)
    return response
