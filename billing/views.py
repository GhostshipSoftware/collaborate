from billing.serializers import *
from billing.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.middleware import csrf
from django.contrib.auth.models import User
# Create your views here.

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve user details
    """

    model = BillingUser
    serializer_class = UserSerializer
    permissions_classes = (permissions.IsAuthenticated)

class AccountListView(generics.ListCreateAPIView):
    """
    Account Listing.  This view lists all accounts currently in the db
    when a GET is performed.

    On a POST request it will create a new account and return the instance
    data back to you.  json required fields for successful post:
    
    first_name
    last_name
    company_name

    """
    model = Account
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AccountCreateUser(APIView):
    """
    /accounts/<pk>/users/

    Create User view for specific accounts.

    This view allows you to list users on an account via a GET
    and create new users via POST.

    REQUIRED FIELDS FOR POST:
    first_name
    last_name
    is_active
    username
    password
    email
    
    """
    model = BillingUser
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get(self, request, pk, format=None):
        """
        Straight forward get of all users attached to this account.
        this is what is called for "/accounts/<pk>/users/".
        """
        account = Account.objects.get(pk=pk)
        users = account.get_users()
        s = UserSerializer(users)
        return Response(s.data)

    def post(self, request, pk, format=None):
        """
        here we take in a pk which links back to an account instance,
        we then use this primary key to look up the account, serialize
        the user object and save it.  Once we save the user, we then
        get the user object, lookup its profile and attach the account 
        id to it.  The account id is gotten from the PK passed to the view
        by the url.

        TODO: Error catching (I.E. passed a bogus key)
        """
        account = Account.objects.get(pk=pk)
        s = UserSerializer(data=request.DATA)
        if s.is_valid():
            s.save()
            user = BillingUser.objects.filter(username=request.DATA['username'])[0]
            user.account = account
            user.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

                    
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token
    
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            csrf_token = csrf.get_token(request)
            account_id = request.user.account_id
            return Response({'token': token.key, 'user': serializer.object['user'].id, 'csrftoken': csrf_token, 'account_id': account_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


