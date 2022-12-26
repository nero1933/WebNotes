from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import redirect

from .models import *

from slugify import slugify

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
    {'title': 'Group notes', 'url_name': 'group_notes'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        self.kwargs['username'] = self.request.user
        # context['folders'] = Folder.objects.filter(user=self.request.user)
        context['folders'] = Folder.objects.filter(user__username=self.kwargs['username']).select_related('user')
        context['notes'] = Note.objects.filter(user__username=self.kwargs['username']).select_related('user')

        if 'note_selected' not in context:
            context['note_selected'] = 0
        elif 'folder_selected' not in context:
            context['folder_selected'] = 0

        return context


class DataAssignMixin:
    def form_valid(self, form, url):
        obj = form.save(commit=False)
        obj.slug = slugify(obj.title)
        obj.user = self.request.user
        obj.save()
        return redirect(url)


# class MultiSlugMixin:
#     pk_url_kwarg = 'pk'
#     slug_url_kwargs = {'slug': 'slug'}  # {slug_field: slug_url_kwarg}
#     query_pk_and_slug = False
#
#     def get_object(self, queryset=None):
#         if queryset is None:
#             queryset = self.get_queryset()
#
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         slugs = {
#             field: self.kwargs[url_kwarg]
#             for field, url_kwarg in self.slug_url_kwargs.items()
#         }
#
#         if pk is not None:
#             queryset = queryset.filter(pk=pk)
#
#         if slugs and (pk is None or self.query_pk_and_slug):
#             queryset = queryset.filter(**slugs)
#
#         if pk is None and not slugs:
#             raise AttributeError(
#                 "Generic detail view %s must be called with either an object "
#                 "pk or a slug in the URLconf." % self.__class__.__name__
#             )
#
#         try:
#             obj = queryset.get()
#         except queryset.model.DoesNotExist:
#             raise Http404("No %(verbose_name)s found matching the query" %
#                           {'verbose_name': queryset.model._meta.verbose_name})
#         return obj
