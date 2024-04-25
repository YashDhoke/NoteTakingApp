from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Note
from .serializers import NoteSerializer
from rest_framework import status, generics
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class  NotesListView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = '__all__'
    ordering = ['-created_at']
    filterset_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class NotesDetailView(APIView):
    model = Note
    serializer_class = NoteSerializer

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = self.serializer_class(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = self.serializer_class(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response({'message': 'note deleted'}, status=status.HTTP_204_NO_CONTENT)


