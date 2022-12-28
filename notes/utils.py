from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import redirect

from .models import *

from re import findall
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
        context['folders'] = Folder.objects.filter(user__username=self.kwargs['username']).select_related('user')
        context['notes'] = Note.objects.filter(user__username=self.kwargs['username']).select_related('user')

        return context


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
                duplicate = findall(r'(?:\-)(\d{2})(?<=$)', slug)[0]
                slug = slug[:-2] + str(int(duplicate) + 1).rjust(2, '0')
                obj = model.objects.get(user=user_id, slug=slug)

        except model.DoesNotExist:
            return slug

    def form_valid(self, obj, form, url):
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.slug = self.slug_check(obj, self.request.user.pk, slugify(form_obj.title))
        form_obj.save()
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
