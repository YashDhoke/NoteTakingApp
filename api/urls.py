from django.urls import path, include

urlpatterns = [

    path('notes/', NotesListView.as_view(), name='notes_list'),
    path('notes/<int:pk>/', NotesDetailView.as_view(), name='notes_detail'),

]