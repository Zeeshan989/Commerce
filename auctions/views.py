from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import *
from .forms import *
from django.contrib import messages
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

def index(request):
    lists=Listing.objects.all()
    watchlist_count = Watchlist.objects.filter(userw=request.user.username).count()
    return render(request, "auctions/index.html", {'lists': lists,'count':watchlist_count})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create(request):
     if request.method == "POST":
         form = kin(request.POST)  # Create an instance of the form with the POST data
         if form.is_valid():  # Check if the form data is valid
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            # Use the form data as needed
            # Example: Saving the form data to a model
            username = request.user.username  # Get the username of the logged-in user
            lis = Listing(title=title, description=description, category=category, starting_bid=starting_bid, image_url=image_url, l_uid=username)
            lis.save() 
            return HttpResponseRedirect(reverse("index"))

     else:
         lin=kin()
         watchlist_count = Watchlist.objects.filter(userw=request.user.username).count()
         return render(request, "auctions/listing.html", {'form': lin,'count':watchlist_count})

@login_required    
def detail(request, id):
    lest = Listing.objects.get(pk=id)
    watchlist_count = Watchlist.objects.filter(userw=request.user.username).count()
    bdi = Bid.objects.filter(bpid=lest.id).first()  # Check if a bid already exists
    if not bdi:
        bdi = Bid(bd=lest.starting_bid, biduid=request.user.username, bpid=lest.id)
        bdi.save()
    winner_bid = Winnerbid.objects.filter(pid=id).values_list('winner', flat=True).first()
    if (lest.l_uid != request.user.username) and (not winner_bid):
        flag = 1
        if request.method == "POST":
            if "bid" in request.POST:
                bid = int(request.POST["bid"])
                highest_bid = Bid.objects.filter(bpid=lest.id).aggregate(max_bid=Max('bd'))['max_bid']
                if bid > highest_bid:
                    b = Bid(bd=bid, biduid=request.user.username, bpid=lest.id)
                    b.save()
                    return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))
                else:
                    t2=2
                    return render(request, "auctions/fail.html",{'count':watchlist_count,'t2':t2})
                
            elif "comment" in request.POST:
                cmt = request.POST["comment"]
                c = CommentContent(prid=id, ct=cmt,userc=request.user.username)
                c.save()
                return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))
            elif "watchlist" in request.POST:
                prwd_list = Watchlist.objects.filter(userw=request.user.username).values_list('prwd', flat=True)
                prodid=int(request.POST["watchlist"])
                if prodid in prwd_list:
                    t=1
                    return render(request, "auctions/fail.html",{'count':watchlist_count,'t':t})
                        
                else:
                    w= Watchlist(prwd=id,userw=request.user.username,wt=lest.title,il=lest.image_url)
                    w.save()
                    return HttpResponseRedirect(reverse("detail", kwargs={'id': id}))

        else:
            try:
               cmmt = CommentContent.objects.filter(prid=id)
            except ObjectDoesNotExist:
                cmmt = None
            bid_ct = Bid.objects.filter(bpid=id).count()
            bid_count=bid_ct-1
            return render(request, "auctions/detail.html", {'listd': lest, 'bid_count': bid_count, 'flag': flag, 'cmmt': cmmt,'count':watchlist_count})
    
    


    elif (lest.l_uid == request.user.username) and (not winner_bid):
        if request.method == "POST":
            max_bid = Bid.objects.filter(bpid=id).aggregate(max_bid=Max('bd'))['max_bid']
            winnerid = Bid.objects.filter(bpid=id, bd=max_bid).values_list('biduid', flat=True).first()
            winner = Winnerbid(pid=id,winner=winnerid)
            winner.save() 
            listing = Listing.objects.get(id=lest.id)
            listing.closed = 'CLOSED'
            listing.save()
            message3='Listing Closed by Owner'
            return render(request, "auctions/detail.html", {'message3': message3, 'listd': lest,'count':watchlist_count})
        else:
            check = 1
            return render(request, "auctions/detail.html", {'check': check, 'listd': lest,'count':watchlist_count})

    elif (request.user.username==winner_bid) and (winner_bid):
        message1 = 'CONGRATS'
        return render(request, "auctions/detail.html", {'message1': message1, 'listd': lest,'count':watchlist_count})

    elif (request.user.username!=winner_bid) and (winner_bid):
        message2 = 'THE LISTING IS CLOSED'  
        return render(request, "auctions/detail.html", {'message2': message2, 'listd': lest,'count':watchlist_count})
    

@login_required    
def categories(request):
    watchlist_count = Watchlist.objects.filter(userw=request.user.username).count()
    if request.method == "POST":
        if "toys" in request.POST:
            toys_listings = Listing.objects.filter(category="Toys", closed="")
            f1=1
            return render(request, "auctions/catresult.html", {'f1':f1, 'toys': toys_listings,'count':watchlist_count})
        elif "electronics" in request.POST:
            e_listings = Listing.objects.filter(category="Electronics", closed="")
            f2=2
            return render(request, "auctions/catresult.html", {'f2':f2, 'electronics': e_listings,'count':watchlist_count})
        elif "home" in request.POST:
            h_listings = Listing.objects.filter(category="Home", closed="")
            f3=1
            return render(request, "auctions/catresult.html", {'f3':f3, 'homes': h_listings,'count':watchlist_count})
        elif "fashion" in request.POST:
            f_listings = Listing.objects.filter(category="Fashion", closed="")
            f4=1
            return render(request, "auctions/catresult.html", {'f4':f4, 'fashions': f_listings,'count':watchlist_count})
    else:
        return render(request, "auctions/categories.html")
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Watchlist

@login_required
def watchlist(request):
    watchlist_count = Watchlist.objects.filter(userw=request.user.username).count()
    if request.method == "POST":
        prodid = int(request.POST["productid"])
        watchlist_item = get_object_or_404(Watchlist, userw=request.user.username, prwd=prodid)
        watchlist_item.delete()
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        watchlist_items = Watchlist.objects.filter(userw=request.user.username)
        return render(request, "auctions/watchlist.html", {'watchitems': watchlist_items, 'count': watchlist_count})







