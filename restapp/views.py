from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes, \
    parser_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .serializers import UserSerializer, ProductsSerializer
from .models import Products
from rest_framework.parsers import JSONParser


@csrf_protect
@api_view(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('UserName')
        password = request.POST.get('Password')
        print(password)
        roles = []
        try:
            userDetails = User.objects.get(username=username)
            print(userDetails.password)
            if check_password(password, userDetails.password):
                print(userDetails.id)
                token = Token.objects.get(user_id=userDetails.id)
                authorizationKey = token.key
                print(authorizationKey)
                if userDetails.is_staff:
                    roles.append('staff')
                if userDetails.is_superuser:
                    roles.append('superuser')
                roles.append('put Products')
                roles.append('Post Products')
                roles.append('delete Products')
                roles.append('get Products')

                userSerializer = UserSerializer(userDetails)
                userData = {}
                userData.update(userSerializer.data)
                userData.update({'Authentication Key': authorizationKey})
                userData.update({'Roles': roles})
                return Response(json.dumps(userData, indent=2))

            else:
                return render(request, 'login.html', {'err_msg': 'Invalid Password'})
        except Exception as e:
            return render(request, 'login.html', {'err_msg': e})
    else:
        return render(request, 'login.html', {})


@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('UserName')
        print(username)
        password = request.POST.get('Password')
        firstName = request.POST.get('firstName')
        print(firstName)
        lastName = request.POST.get('lastName')
        email = request.POST.get('Email')
        userType = request.POST.get('userType')
        if userType == 'normalUser':
            details = User.objects.create_user(username=username, password=password, email=email)
            details.is_staff = False
            details.is_superuser = False
            details.first_name = firstName
            details.last_name = lastName
            details.save()
            det = User.objects.get(username=username)
            print(det.id)
            token_gen = Token.objects.create(user_id=det.id)
            token_gen.save()
            token = Token.objects.get(user_id=det.id)
            authorizationKey = token.key
            print(authorizationKey)
        else:
            details = User.objects.create_superuser(username=username, password=password, email=email)
            details.is_staff = True
            details.is_superuser = True
            details.first_name = firstName
            details.last_name = lastName
            details.save()
            det = User.objects.get(username=username)
            print(det.id)
            token_gen = Token.objects.create(user_id=det.id)
            token_gen.save()
            token = Token.objects.get(user_id=det.id)
            authorizationKey = token.key
            print(authorizationKey)
        return render(request,'register.html',{'sucess_msg':"User Created Sucessful"})
    else:
        return render(request, 'register.html', {})


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getProducts(request):
    if request.user.is_authenticated:
        try:
            productDetails = Products.objects.all()
            produtSerilizer = ProductsSerializer(productDetails, many=True)
            return Response(produtSerilizer.data)
        except Exception as e:
            return Response(json.dumps({'Error ': 'Does not exist'}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getProduct(request, product_id):
    if request.user.is_authenticated:
        try:
            productDetails = Products.objects.get(pk=product_id)
            produtSerilizer = ProductsSerializer(productDetails)
            return Response(produtSerilizer.data)
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def getUsers(request):
    if request.user.is_authenticated:
        try:
            userDetails = User.objects.all()
            print(userDetails)
            userSerilizer = UserSerializer(userDetails, many=True)
            print(userSerilizer.data)
            return Response(userSerilizer.data)
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def getUser(request, user_id):
    if request.user.is_authenticated:
        try:
            userDetails = User.objects.get(pk=user_id)
            print(userDetails)
            userSerilizer = UserSerializer(userDetails)
            print(userSerilizer.data)
            return Response(userSerilizer.data)
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteProduct(request, product_id):
    if request.user.is_authenticated:
        try:
            productDetails = Products.objects.get(pk=product_id)
            productDetails.delete()

            return Response(json.dumps({"Msg": "Product Deleted"}))
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def deleteUser(request, user_id):
    if request.user.is_authenticated:
        try:
            userDetails = User.objects.get(pk=user_id)
            userDetails.delete()
            return Response(json.dumps({"Msg": "User Deleted"}))
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createProduct(request):
    if request.user.is_authenticated:
        try:
            productName = request.POST.get('productName')
            productCategory = request.POST.get('productCategory')
            productCount = request.POST.get('productCount')
            productDetails = Products(productName=productName, productCategory=productCategory,
                                      productCount=productCount)
            productDetails.save()

            return Response(json.dumps({"Msg": "Product Created"}))
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateProduct(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Products.objects.get(pk=product_id)
            data = JSONParser().parse(request)
            print(data)
            print(type(data))
            serilizer = ProductsSerializer(product, data=data)
            print(serilizer.is_valid())
            #print(serilizer.error_messages)
            if serilizer.is_valid():
                serilizer.save()
                return Response(json.dumps({"Msg": "Product Updated"}))
            else:
                return Response(json.dumps({'Msg': 'Enter Valid data'}))

        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))

@api_view(['POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def createUser(request):
    if request.user.is_authenticated:
        try:
            data = JSONParser().parse(request)
            username = data['UserName']
            password = data['Password']
            email = data['Email']
            firstName = data['firstName']
            lastName = data['lastName']
            userType = data['userType']
            if userType == 'normalUser':
                details = User.objects.create_user(username=username, password=password, email=email)
                details.is_staff = False
                details.is_superuser = False
                details.first_name = firstName
                details.last_name = lastName
                details.save()
                det = User.objects.get(username=username)
                print(det.id)
                token_gen = Token.objects.create(user_id=det.id)
                token_gen.save()
                token = Token.objects.get(user_id=det.id)
                authorizationKey = token.key
                print(authorizationKey)
            else:
                details = User.objects.create_superuser(username=username, password=password, email=email)
                details.is_staff = True
                details.is_superuser = True
                details.first_name = firstName
                details.last_name = lastName
                details.save()
                det = User.objects.get(username=username)
                print(det.id)
                token_gen = Token.objects.create(user_id=det.id)
                token_gen.save()
                token = Token.objects.get(user_id=det.id)
                authorizationKey = token.key
                print(authorizationKey)
            return Response(json.dumps({"Msg":"User Created "}))
        except Exception as e:
            return Response(json.dumps({'Error Msg': e}))
    else:
        return Response(json.dumps({'Error Message': 'Unauthrized User'}))
