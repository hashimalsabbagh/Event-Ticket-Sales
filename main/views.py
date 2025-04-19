from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import F
from django.contrib import messages

def home(request): 
    user_id = request.session.get('user_id')
    user = None
    if user_id: 
        try: 
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    return render(request, 'main/home.html', {'user' : user})


def register(request): 
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth_login(request, new_user)
            Wallet.objects.create(user=new_user, money=0.00)
            return redirect('home')
    else: 
        form = UserForm()
    return render(request, 'main/register.html', {'form' : form})

def login(request): 
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form':form})

@login_required
def logoutt(request):
    logout(request)
    return redirect('home')


def viewEvents(request): 
    events = Events.objects.all().order_by('-release_date')[:5]
    if request.user.is_authenticated:
     bought = TicketsPurchased.objects.filter(user=request.user).values_list('event_id', flat=True) # check if user bought the tickets
     return render(request, 'main/events.html', {'events' : events, 'bought' : bought})
    return render(request, 'main/events.html', {'events' : events})


@login_required
def buyTickets(request, id): 
    if request.method == 'POST': 
        quantity = int(request.POST.get('quantity', 1))
        wallet = Wallet.objects.get(user=request.user)
        event = get_object_or_404(Events, id=id)
        if TicketsPurchased.objects.filter(user=request.user, event=event).exists():    # check if user bought tickets 
            messages.error(request, "You already bought tickets")
            return redirect('viewEvents')
        if quantity <= 0:
            messages.error(request, "Please enter a valid number")  #if quantity is 0 or less
            return redirect('viewEvents')
        if quantity > 10: 
            messages.error(request, "You are only allowed a maximum of 10 tickets")   # don't allow more than 10 ticket purchases
            return redirect('viewEvents')
        if event.tickets_no >= quantity:
            if quantity * event.price > wallet.money:   # checks if user has enough money. if not: redirect and show error message 
                messages.error(request, "You don't have enough money")
                return redirect('viewEvents')
            else: 
             Events.objects.filter(id=id).update(tickets_no=F('tickets_no') - quantity)  # update the number of tickets
             TicketsPurchased.objects.create(
                user = request.user,                 # record the purchase in DB
                event = event, 
                quantity = quantity
             )
             Transactions.objects.create(
                 wallet = Wallet.objects.get(user=request.user),   # record transaction
                 amount = (quantity * event.price) * -1
             )
             Wallet.objects.filter(user=request.user).update(money=F('money') - (quantity * event.price)) #  deduct the total amount from user's wallet
             messages.success(request, f"You bought {quantity} ticket(s)!")
        else:
            messages.error(request, "Not enough tickets available")
    return redirect('viewEvents')

@login_required
def viewReservations(request): 
    events = TicketsPurchased.objects.filter(user=request.user).order_by('event__end_date')  # view user's reservations
    requests = CancellationRequest.objects.filter(user = request.user)

    request_map = {req.reservation.id: req for req in requests if req.reservation is not None}
    return render(request, 'main/reservations.html', {'events' : events, 'request_map' : request_map, 'requests': requests})

@login_required
def cancelReservation(request, id): 
    reservation = get_object_or_404(TicketsPurchased, id=id)
    if not CancellationRequest.objects.filter(reservation=reservation).exists():
        CancellationRequest.objects.create(
            reservation=reservation,
            user = request.user,                                                            # if user didn't refund request already, create the request 
            event_name = reservation.event.event_name,
            event_description = reservation.event.event_description,
            quantity = reservation.quantity                              
        )

    return redirect('viewReservations')

@login_required
def viewWallet(request):
    cash = Wallet.objects.get(user=request.user)
    transactions = Transactions.objects.filter(wallet = cash).order_by('-created_at')[:5]

    return render(request, 'main/wallet.html', {'cash': cash, 'transactions' : transactions})


@login_required
def addWallet(request): 
    if request.method == 'POST':
     addCash = float(request.POST.get('addCash', 0.00))
     if addCash > 10000: 
         messages.error(request, "You went over the maximum amount")     # limit only to $10k per transaction 
         return redirect('viewWallet')
     
     Wallet.objects.filter(user=request.user).update(money=F('money') + addCash)  #updates the money user has
     Transactions.objects.create(
         wallet = Wallet.objects.get(user=request.user),  # record transaction
         amount = addCash
     )
    return redirect('viewWallet')
     
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manageCancellation(request): 
   requests =  CancellationRequest.objects.filter(accepted__isnull=True)
   return render(request, 'main/manageCancellation.html', {'requests': requests})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_cancellation(request, id): 
    cancel_request = get_object_or_404(CancellationRequest, id=id)
    
    reservation = cancel_request.reservation
    event = reservation.event

    Wallet.objects.filter(user=reservation.user).update(money=F('money') + (reservation.quantity * event.price))   # add back money to user 
   
    Events.objects.filter(id=reservation.event.id).update(
    tickets_no=F('tickets_no') + reservation.quantity      # add back tickets to events
    )

    Transactions.objects.create(
        wallet = Wallet.objects.get(user=reservation.user),
        amount = (reservation.quantity * event.price)   # record transaction
    )

    CancellationRequest.objects.filter(id=id).update(accepted=True)

    reservation.delete()

    return redirect('manageCancellation')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def reject_cancellation(request, id): 

    CancellationRequest.objects.filter(id=id).update(accepted=False)

    return redirect('manageCancellation')



# Create your views here.
