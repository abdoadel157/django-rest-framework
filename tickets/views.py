
from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse, Http404
from .models import Guest,Movie,Reserveration,Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializers,ReserverationSerializers,MovieSerializers,PostSerializers
from rest_framework.response import responses, Response
from rest_framework import status,filters
from rest_framework.views import APIView
from rest_framework import generics,mixins,viewsets
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from  rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
def no_rest_no_model(request):
    guests=[
        {
            'id':1,
            'name':'omar',
            'mobile':23141413,
        },
        {
            'id':2,
            'name':'yassin',
            'mobile':12312314,

        }

    ]
    return JsonResponse(guests,safe=False)


def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        'guests':list(data.values('name','mobile'))
    }
    return JsonResponse(response)



@api_view(['GET','POST'])
def FBV_List(request):
    #Get
   if request.method=='GET':
     guests=Guest.objects.all()
     serializer=GuestSerializers(guests,many=True)
     return Response(serializer.data)

   elif request.method == 'POST':
        serializer=GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)



# GET , PUT , DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
           return Response(status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
        serializer = GuestSerializers(guest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GuestSerializers(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CBV_List(APIView):
    def get(self,request):
        guest=Guest.objects.all()
        serializer=GuestSerializers(guest,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CBV_pk (APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializers(guest)
        return Response(serializer.data)

    def put(self,request,pk):
       guest = self.get_object(pk)
       serializer=GuestSerializers(guest,data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Mixins_List(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request,pk):
        return self.retrieve(request)

    def put(self, request,pk):
        return self.update(request)

    def delete(self, request,pk):
        return self.destroy(request)


class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends = [filters.SearchFilter]
    search_fields=['movie','hall']

class  viewsets_reservaton(viewsets.ModelViewSet):
    queryset = Reserveration.objects.all()
    serializer_class = ReserverationSerializers

class Post_Pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthorOrReadOnly]

@api_view(['GET'])
def search_movie(request):
    movie=Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    serializer=MovieSerializers(movie)
    return Response(serializer.data)




@api_view(['POST'])
def create_reservation(request):

    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )

    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()

    reservation=Reserveration()
    reservation.guest=request.data['guest']
    reservation.movie=request.data['movie']
    reservation.save()





