#for creating and logging user
import email
from django.contrib.auth import authenticate, login, logout
#intergrityerror for no ducplicate or repeated user
from django.db import IntegrityError
from django.db.models.query import RawQuerySet
#this return http response
from django.http import HttpResponse, HttpResponseRedirect
#this is use for rendering template or htmls
from django.shortcuts import render
#this is use to reverse the url path Ex. from views to url
from django.urls import reverse
#for messages alerts
from django.contrib import messages
from .models import User, ShoppingList, Comments
from django.core.mail import send_mail

def index(request):
    """
    ShoppingList.object.filter it filter all the listings
    in the database that is active meaning the listing is still open for bidding
    is_closed = False means it is still active
    """
    active_listings = ShoppingList.objects.filter(is_closed=False)
    return render(request, "quanta/home.html",{
            "active_listings": active_listings
        })

def quanta_home(request):
    """
    ShoppingList.object.filter it filter all the listings
    in the database that is active meaning the listing is still open for bidding
    is_closed = False means it is still active
    """

    active_listings = ShoppingList.objects.filter(is_closed=False)
    return render(request, "quanta/home_page.html",{
            "active_listings": active_listings,
        })

def contact(request):
    if request.method == "POST":
        message_name = request.POST['contact_name']
        message_subj = request.POST['contact_subject']
        message_email = request.POST['contact_email']
        message = request.POST['contact_message']

        send_mail(
            message_subj,
            'Hi I am '+message_name+ " \n"+message + '\n\n' +'from '+ message_email,
            'from@gmail.com',
            ['lamirageinnandsuite@gmail.com'],
            fail_silently=False,)
        
        return render(request, "quanta/home.html",{
        })

def submit_listings(request):
    if request.method == "POST":
        """
        This fuction get all the value from the input tag
        Using the name attribute in the input tag Ex. [name =item_name], category, description etc.
        """
        item_name = request.POST['item_name']
        user = request.user #this reference the object in User model
        category = request.POST['category']
        description = request.POST['description']
        product_img = request.FILES.get('product_img')
 
        starting_price = request.POST['bid'] #we are storing first bid to the starting price
        listing = ShoppingList(item_name=item_name,description=description, owner=user,
        starting_price = starting_price, is_closed = False, product_img = product_img, category = category)
        listing.save()
    
        return HttpResponseRedirect(reverse("quanta_home"))
        #the user will return to the index after they submit it otherwise
    #they will remain to the creatlist page
    return render(request, "quanta/createlist.html")

def category(request):
   if request.method == "POST":
       #chosen_category takes the value from the selector tag using its name attribute
        chosen_category = request.POST["category"]
        #This will filter all the active list becuase of the boolean object is_close
        active_listings = ShoppingList.objects.filter(is_closed=False,category=chosen_category)
        
        return render(request, "quanta/home_page.html",{
            "active_listings": active_listings
        })

def category_all_list(request):
    if request.method == "POST":
        #chosen_category takes the value from the selector tag using its name attribute
        chosen_category = request.POST['category']
        #This will filter all the specific category closed or active list
        all_listings = ShoppingList.objects.filter(category=chosen_category)

        return render(request,"quanta/all_list.html",{
            "all_listings": all_listings
        })

def display_list(request, listing_id):
    listing = ShoppingList.objects.get(pk = listing_id)
    #this will get all the comments
    comments = listing.comments.all()

    if request.user == listing.owner:
        listing_owner = True
    else:
        listing_owner = False

    listing_in_user_add_to_cart = request.user in listing.add_to_cart.all()
    return render(request, "quanta/display_list.html",{
        'listing':listing,
        'listing_in_user_add_to_cart':listing_in_user_add_to_cart,
        'listing_owner': listing_owner,
        'comments':comments
    })

def add_add_to_cart(request, listing_id):
    user = request.user
    listing = ShoppingList.objects.get(pk = listing_id)
    listing.add_to_cart.add(user) 

    messages.success(request,"+add_to_cart added Successfully!")
    """
    adding the user to the add_to_cart to reference the listing
    Whenever the user is loggged in all the list(add_to_cart) that link to it(user)
    will display to the add_to_cart page.
    because add_to_cart is using Many to many field 
    it can have multiple user and the user can have multiple add_to_cart
    """
    #after adding the listing to the add_to_cart it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def add_comment(request,listing_id):
    if request.method == "POST":
        #get the comment from the input text with the name attribute 'comment'
        comment = request.POST['comment']
        user = request.user #get the user
        #using the listing_id it will get the ShoppingList that we want to add some comment
        listing = ShoppingList.objects.get(pk = listing_id)
        #this will create/save the new comment
        new_comment = Comments(commentor = user, listings = listing,text = comment)
        new_comment.save()# we need to save it to the data base for later reference
        return HttpResponseRedirect(reverse("display_list",args=(listing_id,)))



def remove_add_to_cart(request, listing_id):
    user = request.user
    listing = ShoppingList.objects.get(pk = listing_id)  
    listing.add_to_cart.remove(user) 

    messages.success(request,"-add_to_cart removed Successfully!")
    """
    removing the link of the listing to the user.
    """
    #after removing the listing to the add_to_cart of the user it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def closed_auction(request, listing_id):
    listing = ShoppingList.objects.get(pk = listing_id)
    listing.is_closed = True
    listing.save()
    
    return HttpResponseRedirect(reverse('display_list', args=[listing_id]))

# add profile to model
def view_profile(request):
    user = request.user
    print(user)
    listing = ShoppingList.objects.filter(owner = user)
    return render(request, "quanta/profile_page.html",{"listing":listing})

def user_products(request):
    user = request.user
    print(user)
    listing = ShoppingList.objects.filter(owner = user)
    return render(request, "quanta/my_products.html",{"listing":listing})
# def place_bid(request,listing_id):
#     if request.method == 'POST':
#         listing = ShoppingList.objects.get(pk= listing_id)
#         new_bid = bid = int(request.POST['new_bid'])
#         current_bid = listing.bid.bid

#         if new_bid > current_bid:
#             update_bid = Bid(bid= new_bid, user = request.user)
#             update_bid.save()
#             listing.bid = update_bid
#             listing.save()
#             messages.success(request,"Bid successfully added!")
#             return HttpResponseRedirect(reverse('display_list',args=[listing_id]))
#         else:
#             messages.error(request,"Your Bid Denied! To LOW!")
#             return HttpResponseRedirect(reverse('display_list',args=[listing_id]))


def add_to_cart(request): 
    user = request.user
    user_add_to_cart = user.added_to_cart.all()
    return render(request, "quanta/add_to_cart.html",{
        'user_add_to_cart': user_add_to_cart
    })
    
    
def createlist(request):
    return render(request, "quanta/createlist.html")


def all_list(request):
    all_listings = ShoppingList.objects.all()
    return render(request, "quanta/all_list.html",{
        'all_listings': all_listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully!")
            return HttpResponseRedirect(reverse("quanta_home"))
        else:
            messages.error(request, "Invalid username and/or password!")
            return HttpResponseRedirect(reverse('quanta_home'))
    else:
        return render(request, "quanta/home_page.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("quanta_home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            messages.error(request, "Password Must Match")
            return render(
                request, "qunata/home_page.html", {
                    "username": username,
                    "email": email,
                })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username Already taken!")
            return render(
                request, "quanta/home_page.html", {
                    "username": username,
                    "email": email,
                })
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Registered Successfully!")
            return HttpResponseRedirect(reverse("quanta_home"))
    else:
        return render(request, "quanta/home_page.html")



