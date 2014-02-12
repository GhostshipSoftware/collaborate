from billing.serializers import *
from billing.models import *
from chat.models import *
from issue_tracker.models import *
from tasklist.models import *
from ticketing.models import *
from django.shortcuts import *
from django.contrib.auth.models import User


def index(request):
    """
    main splash view.  Passes all acount info to the index template.
    """

    #first we need an account id.
    user = request.user
    try:
        account_id = user.account_id
    except AttributeError:
        account_id = None

    chatrooms = Channel.objects.filter(account=account_id)
    tickets = TicketQueue.objects.filter(account=account_id)
    issues = IssueManager.objects.filter(account=account_id)
    
    if len(chatrooms) > 0:
        has_channels = True
    else:
        has_channels = False
    if len(tickets) > 0:
        has_tickets = True
    else:
        has_tickets = False
    if len(issues) > 0:
        has_issues = True
    else:
        has_issues = False

    if user.is_authenticated():
        return render_to_response("index.html", {"has_channels": has_channels, "has_tickets": has_tickets, "has_issues": has_issues, "channels": chatrooms, "ticket_queues": tickets, "issuer_managers": issues , 'user': user})
    else:
        return redirect('/accounts/login/')


def manage(request):
    user = request.user
    account_id = user.account_id
    account = Account.objects.get(id=account_id)
    users = account.get_users()
    channels = Channel.objects.filter(account=account_id)

    if user.is_authenticated():
        return render_to_response("manage.html", {"user": user, "account": account, "users": users, 'channels': channels})
    else:
        return redirect('/accounts/login/')
    
def user_detail(request):
    user = request.user
    if request.method == "GET":
        uid = request.GET['uid']
        user = BillingUser.objects.get(id=uid)

    return render_to_response("user-detail.html", {"user": user})


