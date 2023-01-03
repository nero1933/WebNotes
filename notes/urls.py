from django.urls import path, include
# from django.contrib.auth import

from .views import *
urlpatterns = [
    path('', index, name='home'),

    path('private_notes/', PrivateNotes.as_view(), name='private_notes'),
    path('private_notes/<slug:username>/<slug:note_slug>/', ShowNote.as_view(), name='show_note'),
    path('private_notes/<slug:username>/<slug:note_slug>/update/', UpdatePrivateNote.as_view(), name='update_note'),
    path('private_notes/<slug:username>/<slug:note_slug>/delete/', DeletePrivateNote.as_view(), name='delete_note'),
    path('private_notes/add_note/', AddPrivateNote.as_view(), name='add_private_note'),

    path('private_folders/', AllFolders.as_view(), name='all_folders'),
    path('private_folders/<slug:username>/<slug:folder_slug>/', ShowFolder.as_view(), name='show_folder'),
    path('add_private_folder/', AddFolder.as_view(), name='add_folder'),

    path('group_notes/', group_notes, name='group_notes'),
    path('group_notes/add_note/', add_group_note, name='add_group_note'),
    path('group_notes/add_group/', add_group, name='add_group'),
    path('group_notes/add_group_folder/', add_group_folder, name='add_group_folder'),

    path('sign_in/', SignInUser.as_view(), name='sign_in'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),

]

