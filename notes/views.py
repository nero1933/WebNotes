from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from .forms import *
from .utils import *

from slugify import slugify

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
    {'title': 'Group notes', 'url_name': 'group_notes'},
]


def index(request):
    return render(request, 'notes/index.html', {'menu': menu, 'title': 'Home Page'})


# class WomenHome(DataMixin, ListView):
#     model = Women
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Главная страница")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_queryset(self):
#         return Women.objects.filter(is_published=True).select_related('cat')


#  return Note.objects.filter(user=self.request.user, folder__slug=self.kwargs['folder_slug']).select_related('folder')

class PrivateNotes(LoginRequiredMixin, DataMixin, ListView):
    model = Note
    template_name = 'notes/private_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Private Notes')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user.id)
        # return Note.objects.filter(user__username='username').select_related('user')


class ShowNote(LoginRequiredMixin, DataMixin, DetailView):
    model = Note
    template_name = 'notes/show_note.html'
    context_object_name = 'note'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['note'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        try:
            return Note.objects.get(user=self.request.user.id, slug=self.kwargs.get('note_slug', None))
        except self.model.DoesNotExist:
            raise Http404("No note found matching the query")


class AddPrivateNote(LoginRequiredMixin, DataMixin, DataAssignMixin, CreateView):
    form_class = AddPrivateNoteForm
    template_name = 'notes/add_private_note.html'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Private Notes')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(form, 'private_notes')

    def get_form_kwargs(self):
        kwargs = super(AddPrivateNote, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class AllFolders(LoginRequiredMixin, DataMixin, ListView):
    model = Folder
    template_name = 'notes/all_folders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='All Folders')
        return dict(list(context.items()) + list(c_def.items()))


# class WomenCategory(DataMixin, ListView):
#     model = Women
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c = Category.objects.get(slug=self.kwargs['cat_slug'])
#         c_def = self.get_user_context(title='Категория - ' + str(c.name),
#                                       cat_selected=c.pk)
#         return dict(list(context.items()) + list(c_def.items()))


class ShowFolder(LoginRequiredMixin, DataMixin, ListView):
    model = Note
    template_name = 'notes/show_folder.html'
    context_object_name = 'folder'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        f = Folder.objects.get(user=self.request.user.id, slug=self.kwargs.get('folder_slug', None))
        c_def = self.get_user_context(title='Folder -' + str(f.title), folder_selected=f.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Note.objects.filter(user__username=self.kwargs['username']).select_related('user').select_related('folder')


class AddFolder(LoginRequiredMixin, DataMixin, DataAssignMixin, CreateView):
    form_class = AddFolderForm
    template_name = 'notes/add_folder.html'
    success_url = reverse_lazy('all_folders')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add Folder')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(form, 'all_folders')


def group_notes(request):
    return render(request, 'notes/group_notes.html', {'menu': menu, 'title': 'Group notes', 'template': 'notes/group_notes.html'})


def add_group_note(request):
    return render(request, 'notes/add_group_note.html', {'menu': menu, 'title': 'Add Note', 'template': 'notes/group_notes.html'})


def add_group(request):
    return render(request, 'notes/add_group.html', {'menu': menu, 'title': 'Add Note', 'template': 'notes/group_notes.html'})


def add_group_folder(request):
    return render(request, 'notes/add_group_folder.html', {'menu': menu, 'title': 'Add Note', 'template': 'notes/group_notes.html'})


class SignInUser(DataMixin, CreateView):
    form_class = SignInUserForm
    template_name = 'notes/sign_in.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'notes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def about_us(request):
    return render(request, 'notes/about_us.html', {'menu': menu, 'title': 'About Us'})


def contact_us(request):
    return render(request, 'notes/contact_us.html', {'menu': menu, 'title': 'Contact Us'})
