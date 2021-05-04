from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .serializers import   BookSerializer,FavouriteSerializer,RegistrationSerializers
from rest_framework.response import Response
from .models import Book,Favourite
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
#---------------------------------------------------------token based auth --------------------------------------------#######
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@api_view(['POST'],)
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializers(data = request.data)
        data={}
        if serializer.is_valid():

            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            data['Response'] = "Registration success "
            return Response(data)
    else:
        msg={'msg':"post request bhej bhai "}
        return Response(msg)

@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def logout(request):
    if request.method == "POST":
        print('-------------------------------------------------------------------------------------------------------')
        # print(request.user)
        request.user.auth_token.delete()
        return Response(
            {
                "msg":"you are logout "
            }
        )

#-------------------------------------------------------token based auth end------------------------------------------######

#-------------------------------------------------------api view for book start---------------------------------------#######


@api_view(['GET','POST','PATCH','DELETE','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,IsAuthenticatedOrReadOnly])
def book_api(request,pk=None):
    if request.method == "GET":
        print('--------------------------------------------------------------------')
        print(request.user.is_superuser)
        id = pk
        if id is not None:
            stu = Book.objects.get(id=id)
            serializer  = BookSerializer(stu)
            return Response(serializer.data)
        else:
            stu=Book.objects.all()
            serializer  = BookSerializer(stu,many=True)
            return Response(serializer.data)


    if request.method == "POST":
        print(request.data)
        if request.user.is_superuser:
            serializer = BookSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid(): 
                serializer.save()
                msg= {'msg':'data is inserted check in database'}
                return Response(msg)
            else:
                return Response(serializer.errors)
        else:
            msg= {'msg':'Tum Super User nhi ho keval dekho post na kro '}
            return Response(msg)

        
    if request.method == "PATCH":
        id  = pk
        stu = Book.objects.get(pk=id)
        date ={}
        print(request.data)
        if request.user.is_superuser:
            serializer = BookSerializer(stu,data=request.data,partial=True)
            print(serializer)
            print(stu)
            if request.data == date:
                msg= {'msg':'enter data to update'}
                return Response(msg)
            else:
                print("here")
                if serializer.is_valid():
                    serializer.save()
                    msg= {'msg':'data is updated check in database'}
                    return Response(msg)
                else:
                    return Response(serializer.errors)
        else:
            msg= {'msg':'Tum Super User nhi ho keval dekho update na karo '}
            return Response(msg)
            
    if request.method == "PUT":
        id  = pk
        stu = Book.objects.get(pk=id)
        date ={}
        print(request.data)
        if request.user.is_superuser:
            serializer = BookSerializer(stu,data=request.data,partial=False)
            print(serializer)
            print(stu)
            if request.data == date:
                msg= {'msg':'enter data to update'}
                return Response(msg)
            else:
                print("here")
                if serializer.is_valid():
                    serializer.save()
                    msg= {'msg':'data is updated check in database'}
                    return Response(msg)
                else:
                    return Response(serializer.errors)
        else:
            msg= {'msg':'Tum Super User nhi ho keval dekho update na karo '}
            return Response(msg)


    if request.method == "DELETE":
        id  = pk
        if request.user.is_superuser:
            stu = Book.objects.get(pk=id)
            stu.delete()        
            msg= {'msg':'data is deleted check in database'}
            return Response(msg)
        else:
            msg= {'msg':'Tum Super User nhi ho keval dekho delete na karo '}
            return Response(msg)
#-------------------------------------------------------api view for book end---------------------------------------#######


#-------------------------------------------------------api view for favourite end---------------------------------------#######

@api_view(['GET','POST','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fav_api(request,pk=None):
    if request.method == "GET":
        print(request.user)
        id = pk
        if id is not None:
            stu = Favourite.objects.get(id=id)
            serializer  = FavouriteSerializer(stu)
            if len(stu) == 0:
                msg={'msg':" apka favourite abhi koi  nhi hai phle kuch add kro phir dekho"}
                return Response(msg)
            return Response(serializer.data)
        else:
            print(request.user)
            stu=Favourite.objects.filter(user=request.user)
            print(stu)
            serializer  = FavouriteSerializer(stu,many=True)
            if len(stu) == 0:
                msg={'msg':" apka favourite abhi nhi hai kuch phle add kro phir dekho"}
                return Response(msg)
            return Response(serializer.data)    
    if request.method == "POST":
        print('---------------------------------------------------------------------------')
        print(request.data)
        request.data._mutable = True
        # request.data['book'] = int(request.data['book'])
        # request.data['user'] = int(request.data['user'])
        # print(type(request.data['user']))
        print(type(request.user.id))
        request.data['user'] = int(request.data['user'])
        iscorrectuser = request.data['user'] 
        if iscorrectuser == request.user.id:
            serializer = FavouriteSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                msg= {'msg':'serializer run '}
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            msg= {'msg':'Not permitted '}
            return Response(msg)

        
        
    if request.method == "DELETE":
        id = pk
        # request.data._mutable = True
        # request.data['book'] = int(request.data['book'])
        # request.data['user'] = int(request.data['user'])
        del_book = Favourite.objects.filter(id=id).exists()
        if del_book == True:
            print('---------------------------------------------------------------------------')
            
            del_book = Favourite.objects.get(id=id)
            if request.user == del_book.user:
                del_book.delete()
                msg= {'msg':'delete ho gaya hai database main check kr lo vro '}
                return Response(msg)
                print(del_book)
            else:
                msg= {'msg':' phle permission leke aao '}
                return Response(msg)

        else:
            msg= {'msg':' ye image favourite main nhi store hai '}
            return Response(msg)

#-------------------------------------------------------api view for favourites end---------------------------------------#######

        
