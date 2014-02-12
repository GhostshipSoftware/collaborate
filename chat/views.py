from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
from billing.models import BillingUser
from django.shortcuts import *
from django.http import HttpResponse
from chat.serializers import *
from chat.models import *
from django.views.decorators.cache import cache_control, cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.core.cache import cache

@csrf_exempt
@login_required(login_url="/accounts/login/")
def chat(request):
    channels = Channel.objects.filter(account=request.user.account_id)
    user = request.user
    return render_to_response('chat/index.html', {'channels': channels, 'user': user, 'account': user.account_id}, context_instance=RequestContext(request))

def channel(request):
    channel = request.GET['channel']
    co = Channel.objects.get(pk=channel)
    ao = Account.objects.get(pk=request.user.account_id)
    user = request.user
    return render_to_response('chat/channel.html', {'channel_obj': co, 'channel': channel, 'user': user, 'account': user.account_id, 'account_obj': ao }, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
       
"""
CHANNEL VIEWS
"""

class ChannelListView(generics.ListCreateAPIView):

    model = Channel
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ChannelDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Channel
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
 
    """
    def delete(self, request, pk, format=None):
        channel = Channel.objects.get(pk=pk)
        messages = Message.objects.filter(channel=pk)
        for m in messages:
            m.delete()
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """

class ChannelUserAddView(APIView):
    model = Channel
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def post(self, request, pk, format=None):
        channel = Channel.objects.get(pk=pk)
        new_user = BillingUser.objects.get(pk=request.DATA['user'])
        s = UserSerializer(new_user)
        channel.add_user(s.data)
        return_data = {"response": "User added."}
        return Response(return_data, status=status.HTTP_200_OK)

class ChannelRemoveUserView(APIView):
    model = Channel
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, format=None):
        channel = Channel.objects.get(pk=pk)
        user = BillingUser.objects.get(pk=request.DATA['user'])
        s = UserSerializer(user)
        channel.remove_user(s.data)
        return_data = {"response": "User Removed"}
        return Response(return_data, status=status.HTTP_200_OK)
        
"""
MESSAGE VIEWS
"""
class MessageCreateView(generics.ListCreateAPIView):
    model = Message
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, format=None):
        cversion = cache.get(request.user.id)
        if cversion is None:
            cversion = 1
            cache.set(request.user.id, cversion)
        messages = Message.objects.filter(channel=pk).order_by('-id')[:100]
        messages = reversed(messages)#reverse the list to get proper ordering
        mlist = list(messages) #convert tolist from reversed obj
        s = MessageSerializer(mlist)
        cached_messages = cache.get('channel_%s_messages' % pk, version=cversion)
        if cached_messages is not None:
            if len(cached_messages) < 1:
                cache.set('channel_%s_messages' % pk, s.data, 300, version=cversion)
                cached_messages = cache.get('channel_%s_messages' % pk, version=cversion)
                #response = {'response': "No msgs"}
                #return Response(response, status=status.HTTP_200_OK)

        if cached_messages is None:
            cache.set('channel_%s_messages' % pk, s.data, 300, version=cversion)
            cached_messages = cache.get('channel_%s_messages' % pk, version=cversion)
        last_msg_list = list(mlist)
        try:
            last_msg = last_msg_list[len(last_msg_list) - 1]
        except IndexError:
            last_msg = {'id': 0}
        try:
            last_cache_message = cached_messages[len(cached_messages) -1]
        except IndexError:
            last_cache_message = {'id': 0}
        #print "cm_id(%s), m_id(%s), channel: %s" % (last_cache_message['id'], last_msg.id, pk)
        try:
            if last_cache_message['id'] != last_msg.id:
                cache.set('channel_%s_messages' % pk, s.data, 300, version=cversion+1)
                cached_messages = cache.get('channel_%s_messages' % pk, version=(cversion+1))
                cache.set(request.user.id, (cversion+1))
        except AttributeError:
            pass
        return Response(cached_messages, status=status.HTTP_200_OK)
    

