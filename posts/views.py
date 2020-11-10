from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from .models import Post, Vote
from .serializers import  PostSerializer, VoteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response



class PostList(generics.ListCreateAPIView): #clase based view que va a crear
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):  #esta funcion siempre se llama asi
        serializer.save(poster=self.request.user) # cada vez que guarde un objeto post, voy a poner como poster a cualquiera que haya hecho la api call


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk']) #la pk va a ser cualquiera que yo haya pasado en urls.py , en la parte del path <int:pk>
        return Vote.objects.filter(voter=user, post=post) #buscamos los votos donde el usuario es el mismo que hace el request, y  post sea el mismo que el de linea 24


        #
    def perform_create(self, serializer):  #esta funcion siempre se llama asi

        if self.get_queryset().exists(): #esto es para verificar si el voto emitido por la persona sobre ese post ya existe, osea, si ya votó
            raise ValidationError('you have already voted for this post')

        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk'])) # cada vez que guarde un objeto post, voy a poner como poster a cualquiera que haya hecho la api call



    def delete(self, request, *args, **kwargs):

        if self.get_queryset().exists(): #si existe un voto para este usuario particular, sobre este post particular
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('you never vote for this post')
