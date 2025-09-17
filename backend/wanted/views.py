from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import WantedPerson
from .forms import WantedPersonForm
from django.contrib import messages
from .utils import extract_face_embedding

@login_required
def wanted_list(request):
    query = request.GET.get('q', '')
    if query:
        persons = WantedPerson.objects.filter(full_name__icontains=query).order_by('id')
    else:
        persons = WantedPerson.objects.all().order_by('id')

    paginator = Paginator(persons, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'wanted/wanted_list.html', {'page_obj': page_obj, 'query': query})

@login_required
def wanted_detail(request, pk):
    person = get_object_or_404(WantedPerson, pk=pk)
    return render(request, 'wanted/wanted_detail.html', {'person': person})

@login_required
def wanted_add(request):
    if not request.user.is_staff:
        return redirect('wanted_list')

    if request.method == 'POST':
        form = WantedPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة المطلوب بنجاح!")
            return redirect('wanted_list')
    else:
        form = WantedPersonForm()

    return render(request, 'wanted/wanted_form.html', {'form': form, 'is_edit': False})

@login_required
def wanted_edit(request, pk):
    if not request.user.is_staff:
        return redirect('wanted_list')

    person = get_object_or_404(WantedPerson, pk=pk)
    if request.method == 'POST':
        form = WantedPersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل بيانات المطلوب بنجاح!")
            return redirect('wanted_list')
    else:
        form = WantedPersonForm(instance=person)

    return render(request, 'wanted/wanted_form.html', {'form': form, 'is_edit': True})

@login_required
def wanted_delete(request, pk):
    if not request.user.is_staff:
        return redirect('wanted_list')
    person = get_object_or_404(WantedPerson, pk=pk)
    if request.method == 'POST':
        person.delete()
        messages.success(request, "تم حذف المطلوب بنجاح!")
        return redirect('wanted_list')
    return render(request, 'wanted/wanted_confirm_delete.html', {'person': person})
