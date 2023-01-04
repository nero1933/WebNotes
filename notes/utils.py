from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import redirect

from .models import *

from slugify import slugify

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
    {'title': 'Group Notes', 'url_name': 'group_notes'},
]

sidebar_notes_menu = [
    {'name': 'All', 'url_name': 'private_notes'},
    {'name': 'Add', 'url_name': 'add_private_note'},
]

sidebar_folder_menu = [
    {'name': 'All', 'url_name': 'all_folders'},
    {'name': 'Add', 'url_name': 'add_folder'},
]


class PrivateNoteMixin:
    paginate_by = 9

    @staticmethod
    def get_sidebar_manu(context_item, sidebar_menu):
        """
        If there are no notes the function will remove 'all' link and
        return dict with only 'add' link. If there are notes the function
        will return 'all' and 'add'. Same with the folders.
        context_item - queryset,
        sidebar_menu - dict
        """
        m = sidebar_menu.copy()
        if len(context_item) == 0:
            m.pop(0)

        return m

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['selected_menu'] = 'private_notes'
        self.kwargs['username'] = self.request.user
        context['sidebar_notes'] = Note.objects.filter(user__username=
                                                       self.kwargs['username']).select_related('user')[:5]
        context['sidebar_folders'] = Folder.objects.filter(user__username=
                                                           self.kwargs['username']).select_related('user')[:5]

        context['sidebar_notes_menu'] = self.get_sidebar_manu(context['sidebar_notes'], sidebar_notes_menu)
        context['sidebar_folder_menu'] = self.get_sidebar_manu(context['sidebar_folders'], sidebar_folder_menu)

        return context


class NoteMixin:
    def get_object(self, queryset=None):
        try:
            return Note.objects.get(user=self.request.user.id, slug=self.kwargs.get('note_slug', None))
        except self.model.DoesNotExist:
            raise Http404("No such note")


class DataAssignMixin:
    # model.objects.get() and while loop is probably not the best solution.
    # Maybe counting the identical titles where user is the same
    # and adding duplicate number ('-02') will be better
    @staticmethod
    def slug_check(model, user_id, slug):
        """
        Method is checking is there an object in db with this slug.
        If True: add to slug '-02', if slug with '-02' exists try '-03'.
        Continue until slug will be uniq for the user.
        """
        try:
            obj = model.objects.get(user=user_id, slug=slug)
            slug = obj.slug + '-02'
            obj = model.objects.get(user=user_id, slug=slug)

            while obj:
                duplicate_number = slug[-2:]
                slug = slug[:-2] + str(int(duplicate_number) + 1).rjust(2, '0')
                obj = model.objects.get(user=user_id, slug=slug)

        except model.DoesNotExist:
            return slug

    def form_valid(self, obj, form, url):
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.slug = self.slug_check(obj, self.request.user.pk, slugify(form_obj.title))
        form_obj.save()
        return redirect(url)
