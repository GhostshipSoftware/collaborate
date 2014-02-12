# Create your views here.
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
import urllib2, urllib
from django.shortcuts import *
from django.http import HttpResponse
from ticketing.serializers import *
from ticketing.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

"""
TICKETS VIEWS
"""
class TicketListView(generics.ListCreateAPIView):
    """
    List all ticketss or create a new ticket.
    """
    model = Ticket
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    list details about a specific ticket item.
    """
    model = Ticket
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TicketCommentView(APIView):
    """
    View that accepts post for a new comment to be added
    to the ticket
    """
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        ticket = self.get_object(pk)
        comment = request.DATA['comment']
        ticket.add_comment(comment)
        ticket.save()
        serializer = TicketCommentSerializer(ticket,request.DATA)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
   
"""
TICKET QUEUE VIEWS
"""
class TicketQueueListView(generics.ListCreateAPIView):
    """
    List all ticket queues or create a new queue.
    """
    model = TicketQueue
    serializer_class = TicketQueueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TicketQueueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    List details about a specific ticket queue
    object.
    """

    model = TicketQueue
    serializer_class = TicketQueueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TicketQueueTicketListView(APIView):
    """
    List a ticket queues tickets.  Useful for building
    client views into each queue.
    """
    
    def get_object(self, pk):
        try:
            return TicketQueue.objects.get(pk=pk)
        except TicketQueue.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queue = self.get_object(pk)
        tickets = queue.get_tickets()
        tserializer = TicketSerializer(tickets)
        return Response(tserializer.data, status=status.HTTP_200_OK)


    def post(self, request, pk, format=None):
        queue = self.get_object(pk)
        request.DATA['queue_id'] = queue.id
        ts = TicketSerializer(data=request.DATA)
        if ts.is_valid():
            ts.save()
            response = {"response": "Ticket Created"}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(ts.errors, status=status.HTTP_400_BAD_REQUEST)


