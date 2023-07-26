from django.shortcuts import render
from django.http import Http404, JsonResponse

from .serializers import *
from .models import Guest,Movie,Reservation,Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status ,filters
from rest_framework.views import APIView
from rest_framework import generics , mixins
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from .permissions import  IsAuthorOrReadOnly
# Create your views here.

#1 without REST and no model query FBV
def no_rest_on_models(request):
    data = [
        {"id": 2, "name": "Ahmed", "age": 18},
        {"id": 3, "name": "Salah", "age": 15}
    ]
    return JsonResponse(data, safe=False)


#2  model data default django without rest 
def no_rest_from_models(request):
    guest = Guest.objects.all()
    context = {
        'guest':list(guest.values('name','mobile'))
    }
    return JsonResponse(context)


#List ==GET
#Create == POST
#PK Query == GET
#Update == PUT
#Delete destory == DELETE


#Function based view
#3.1 GET POST
@api_view(['GET',"POST"])
def FBV_LIST(request):
    if request.method=='GET':
        guests=Guest.objects.all()
        serializer =GuestSerializer(guests,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer =GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
#3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest=Guest.objects.get(pk=pk)
    except guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if request.method=='GET':
        serializer =GuestSerializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method=='PUT':
        serializer =GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    elif request.method=='DELETE':
        guest.delete()
        Response(status=status.HTTP_204_NO_CONTENT)

#4 CBV class based view 
#4.1  GET POST
class CBV_List(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer =GuestSerializer(guests,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#4.1  GET PUT DELETE
class CBV_PK(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 5 Mixnis
#5.1 Mixnis List 
class MixnisList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    #Get
    def get(self,request):
        return self.list(request)
    #Post
    def post(self,request):
        return self.create(request)

#5.2 Mixnis Get Put Delete

class Mixnis_Pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    #GET PK
    #Get
    def get(self,request,pk):
        return self.retrieve(request)
    #Put
    def put(self,request,pk):
        return self.update(request)
    #Delete
    def delete(self,request,pk):
        return self.destroy(request)
    
# 6  Generics 
#6.1 Generic Get and Post 
class Generics_List(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes = [TokenAuthentication]

# 6.2 Get Put Delete
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

# viewsets
class viewsets_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
class viewsets_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']
class viewsets_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservatinoSerailizer
    authentication_classes = [TokenAuthentication]

#find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )

    serializer =MovieSerializer(movies,many=True)

    return Response(serializer.data)

# # new Reservation 
# @api_view(['POST'])
# def newreservations(request):
#     # movie = Movie.objects.get(
#     #     hall = request.data['hall'],
#     #     movie = request.data['movie'],
#     # )
#     movie = Movie()
#     movie.hall= request.data['hall']
#     movie.movie=request.data['movie']
#     movie.save()

#     guest = Guest()
#     guest.name =request.data['name']
#     guest.mobile = request.data['mobile']
#     guest.save()

#     reservation = Reservation()
#     reservation.guest = guest
#     reservation.movie = movie
#     reservation.save()

#     return Response(reservation.data,status=status.HTTP_201_CREATED)

@api_view(['POST'])
def newreservations(request):
    # Get or create the Movie instance
    movie, _ = Movie.objects.get_or_create(
        hall=request.data['hall'],
        movie=request.data['movie']
    )

    # Get or create the Guest instance
    guest, _ = Guest.objects.get_or_create(
        name=request.data['name'],
        mobile=request.data['mobile']
    )

    # Create the Reservation instance
    reservation = Reservation.objects.create(
        guest=guest,
        movie=movie
    )

    return Response( status=status.HTTP_201_CREATED)

#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer