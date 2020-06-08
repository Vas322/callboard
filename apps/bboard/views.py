from .forms import BbForm, AIFormSet
from .models import Bb, Rubric, RevRubric
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from callboard.settings import BASE_DIR
from datetime import datetime
import os
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

FILES_ROOT = os.path.join(BASE_DIR, '/media/')


@login_required
def profile(request):
    bbs = Bb.objects.all()
    context = {'bbs': bbs}
    return render(request, 'bboard/profile.html', context)


class BbEditView(UpdateView):
    """Вьюха исправления объявления"""
    model = Bb
    form_class = BbForm
    success_url = '/bboard/detail/{id}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


@login_required()
def edit(request, pk):
    """Вьюха исправления объявления"""

    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
                return HttpResponseRedirect(reverse('by_rubric',
                                                    kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


@login_required
def profile_bb_add(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Объявление добавлено')
                return redirect('index')
    else:
        form = BbForm()
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'bboard/profile_bb_add.html', context)


class BbAddView(LoginRequiredMixin, FormView):
    """Добавление нового объявления"""
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = 'bboard/detail/{id}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbDetailView(DetailView):
    """Детальная информация об объявлении"""
    model = Bb

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbByRubricView(ListView):
    """Вьюха обрабатывающая рубрики"""
    template_name = "bboard/by_rubric.html"
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    """Вьюха удаляет объявление"""
    model = Bb
    form_class = BbForm
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def delete(request, pk):
    """Вьюха удаляет объявление"""
    if request.user.is_authenticated:
        bb = Bb.objects.get(pk=pk)
        if request.method == 'POST':
            bb.delete()
            return HttpResponseRedirect(reverse('by_rubric',
                                                kwargs={'rubric_id': bb.rubric.pk}))
        else:
            context = {'bb': bb}
            return render(request, 'bboard/bb_confirm_delete.html', context)
    else:
        return render(request, 'bboard/login.html')


class BbIndexView(ArchiveIndexView):
    """Вьюха выводит все записи в хронологическом порядке по датам"""
    model = Bb
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def index(request):
    """Вьюха главной страницы с пагинатором"""
    rubrics = RevRubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs,3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
    return render(request, 'bboard/index.html', context)
