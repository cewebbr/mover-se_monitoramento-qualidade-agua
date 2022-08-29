from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import WaterSourceCreateForm
from .models import WaterSource
from django.contrib import messages

# Create your views here.


@login_required
def create_watersource(request):
    if request.method == 'POST':
        waterSourceForm = WaterSourceCreateForm(request.POST)
        if waterSourceForm.is_valid():
            watersource = waterSourceForm.save(commit=False)
            watersource.user = request.user
            watersource.save()
            messages.success(request, 'Nascente cadastrada com sucesso!')
        else:
            messages.info(request, 'Erro ao inserir valores!')
    return render(request, 'watersource/create-watersource.html')


def view_watersource(request, id):
    watersource = get_object_or_404(WaterSource, pk=id)
    return render(request, 'watersource/view-watersource.html', {'watersource': watersource})


def remove_watersource(request):
    watersource_id = request.POST.get("watersource-id", "")
    watersource = get_object_or_404(WaterSource, pk=watersource_id)
    watersource.delete()
    return redirect('web:index')
