from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from .forms import *
from .utils import *

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
    {'title': 'Group notes', 'url_name': 'group_notes'},
]


def index(request):
    return render(request, 'notes/index.html', {'menu': menu, 'title': 'Home Page'})


class PrivateNotes(LoginRequiredMixin, DataMixin, ListView):
    model = Note
    template_name = 'notes/private_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Private Notes', selected='private_notes')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        self.kwargs['username'] = self.request.user
        return Note.objects.filter(user__username=self.kwargs['username']).select_related('user')


class ShowNote(LoginRequiredMixin, DataMixin, DetailView):
    model = Note
    template_name = 'notes/show_note.html'
    context_object_name = 'note'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.folder:
            context['folder_selected'] = self.object.folder.pk
            context['folder_link'] = True

        c_def = self.get_user_context(title='Note: ' + str(context['note']),
                                      note_selected=self.object.pk)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        try:
            return Note.objects.get(user=self.request.user.id, slug=self.kwargs.get('note_slug', None))
        except self.model.DoesNotExist:
            raise Http404("No such note")


class AddPrivateNote(LoginRequiredMixin, DataMixin, DataAssignMixin, CreateView):
    form_class = AddPrivateNoteForm
    template_name = 'notes/add_private_note.html'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add note', selected='add_private_note')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(Note, form, 'private_notes')

    def get_form_kwargs(self):
        kwargs = super(AddPrivateNote, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class UpdatePrivateNote(LoginRequiredMixin, DataMixin, UpdateView):
    model = Note
    template_name = 'notes/update_private_note.html'
    fields = ['title', 'content', 'icon', 'folder']
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Change note')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        try:
            return Note.objects.get(user=self.request.user.id, slug=self.kwargs.get('note_slug', None))
        except self.model.DoesNotExist:
            raise Http404("No such note")


class DeletePrivateNote(LoginRequiredMixin, DataMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_private_note.html'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete note')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        try:
            return Note.objects.get(user=self.request.user.id, slug=self.kwargs.get('note_slug', None))
        except self.model.DoesNotExist:
            raise Http404("No such note")


class AllFolders(LoginRequiredMixin, DataMixin, ListView):
    model = Folder
    template_name = 'notes/all_folders.html'
    context_object_name = 'folders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='All Folders', selected='all_folders')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Folder.objects.filter(user__username=self.request.user).select_related('user')


class ShowFolder(LoginRequiredMixin, DataMixin, ListView):
    model = Note
    template_name = 'notes/private_notes.html'
    context_object_name = 'folder_notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        f = Folder.objects.get(user=self.request.user.id, slug=self.kwargs.get('folder_slug', None))
        c_def = self.get_user_context(title='Folder: ' + str(f.title), folder_selected=f.pk, is_folder=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Note.objects.filter(user__username=self.kwargs['username'],
                                   folder__slug=self.kwargs['folder_slug']
                                   ).select_related('user').select_related('folder')

    def get(self,  *args, **kwargs):
        try:
            return super().get(self,  *args, **kwargs)
        except Folder.DoesNotExist:
            raise Http404('No such folder')


class AddFolder(LoginRequiredMixin, DataMixin, DataAssignMixin, CreateView):
    form_class = AddFolderForm
    template_name = 'notes/add_folder.html'
    success_url = reverse_lazy('all_folders')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add Folder', selected='add_folder')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(Folder, form, 'all_folders')


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
