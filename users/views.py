from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import RegistrationSerializer
from .models import User

@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'User registered successfully'
        data['id'] = user.id
        data['email'] = user.email
        data['full_name'] = user.full_name
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['GET'])
def profile_view(request):
    pass

@api_view(['POST'])
def login(request):
    data = {}
    email = request.data['email']
    password = request.data['password']

    # check if account exists
    try:
        user = User.objects.get(email=email)
    except BaseException as erorr:
        raise ValidationError(
            {'400': '{}'.format(erorr)}
        )

    # get or create new token
    token = str(Token.objects.get_or_create(user=user)[0])
    data['token'] = token

    # check if password is corresct
    if not check_password(password, user.password):
        raise ValidationError(
            {'message': 'Incorect credentials'}
        )
    
    if user:
        data['response'] = 'User logged in successfully'
        data['id'] = user.id
        data['email'] = user.email
        data['full_name'] = user.full_name
        return Response(data)
    else:
        raise ValidationError(
            {'400': 'Account doesnt exist'}
        )

@api_view(['POST'])
def logout(request):
    data = {}
    token = request.data['token']

    # check if token exists
    try:
        tkn = Token.objects.get(key=token)
    except BaseException as error:
        raise ValidationError(
            {'400': '{}'.format(error)}
        )

    # get token user for logout delete token
    user = tkn.user
    if user:
        user.auth_token.delete()
        logout(request._request)
        data['response'] = 'User loged out succesfully'
    else:
        raise ValidationError(
            {'400': 'Something went wrong'}
        )
    return Response(data)