from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import TokenAuthentication
import logging

from .serializers import UserSerializer, LoginSerializer, LibroSerializer, PreferitoSerializer
from api.models import Libro, Preferiti

# Create your views here.
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            
            """
            the underscore _ is simply a convention to indicate that it is not necessary to use or store the second value 
            returned by the get_or_create method. The token variable contains the user's token object, 
            which is what the subsequent code needs.
            """
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key}, status=status.HTTP_200_OK)
            
            #return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
@method_decorator(csrf_exempt, name='dispatch')
class LibroView(APIView):
      
    def get(self, request):
        books = Libro.objects.all()
        #logger.debug(f"Books found: {books}")
        
        """
        The many=True argument indicates that you are dealing with a list of objects rather than a single object.
        """
        serializer = LibroSerializer(books, many = True)
      
        return Response(serializer.data)
    
    def post(self, request, format = None):
        
        if request.user.is_authenticated:
            serializer = LibroSerializer(data=request.data)
        
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Prima di poter creare un nuovo libro devi essere loggato!"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')  
class LibroGetDetails(APIView):
    
    def get_object(self, id):
        book = get_object_or_404(Libro, pk = id)
        
        return book
    
    def get(self, request, id = None):
        book = self.get_object(id)
        serializer = LibroSerializer(book)
        
        return Response(serializer.data)
    
    def put(self, request, id = None):
        book = self.get_object(id)
        serializer = LibroSerializer(book, data = request.data)
        
        if request.user.is_authenticated:
        
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Prima di poter aggiornare un libro devi essere loggato!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id = None):
        
        if request.user.is_authenticated:
        
            book = self.get_object(id)
            book.delete()
            
            return Response({"message": "Libro eliminato correttamente!"}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response({"message": "Prima di poter eliminare un libro devi essere loggato!"}, status=status.HTTP_400_BAD_REQUEST)
        

class PreferitiViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, book_id):
        return get_object_or_404(Libro, pk = book_id)

    # GET /preferiti: Recupera la lista dei libri preferiti dell'utente autenticato
    def list(self, request):
        queryset = Preferiti.objects.filter(utente = request.user)
        serializer = PreferitoSerializer(queryset, many = True)
        
        return Response(serializer.data)

    # POST /preferiti/{book_id}: Aggiunge un libro ai preferiti dell'utente autenticato
    def create(self, request, book_id = None):
        libro = self.get_object(book_id)
        
        preferito, created = Preferiti.objects.get_or_create(utente = request.user, libro = libro)
        
        #created: true or false
        if not created:
            return Response({'error': 'Libro already in favorites'}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = PreferitoSerializer(preferito)
        
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    # DELETE /preferiti/{book_id}: Rimuove un libro dai preferiti dell'utente autenticato
    def destroy(self, request, book_id = None):
        libro = self.get_object(book_id)
        
        preferito = get_object_or_404(Preferiti, utente = request.user, libro = libro)
        preferito.delete()
        
        return Response(status = status.HTTP_204_NO_CONTENT)