#for creating and logging user
import email
from itertools import product
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
from .models import User, ShoppingList, Comments, CheckoutOrder
from django.db.models import Sum
from django.core.mail import send_mail
import datetime

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
    user = request.user
    if user.is_authenticated:
        my_cart_count = user.added_to_cart.all().count()
        my_ship_count = user.customerCheckoutOrder.all().count() 
    else:
        my_cart_count = 0
         
    active_listings = ShoppingList.objects.filter(is_closed=False)
    return render(request, "quanta/home_page.html",{
            "active_listings": active_listings,
            "my_cart_count":my_cart_count,
            "my_ship_count":my_ship_count,
        })

def contact(request):
    if request.method == "POST":
        message_name = request.POST['contact_name']
        message_subj = request.POST['contact_subject']
        message_email = request.POST['contact_email']
        message = request.POST['contact_message']

        messages.success(request,"Message Sent!")
        send_mail(
            message_subj,
            'Hi I am '+message_name+ " \n"+message + '\n\n' +'from '+ message_email,
            message_email,
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
    user = request.user
    if user.is_authenticated:
        my_cart_count = user.added_to_cart.all().count()
        my_ship_count = user.customerCheckoutOrder.all().count() 
    else:
        my_cart_count = 0
    listing_in_user_add_to_cart = request.user in listing.add_to_cart.all()
    listing_in_user_favorites = request.user in listing.favorite.all()
    return render(request, "quanta/display_list.html",{
        'listing':listing,
        'listing_in_user_add_to_cart':listing_in_user_add_to_cart,
        'listing_in_user_favorites':listing_in_user_favorites,
        'listing_owner': listing_owner,
        'comments':comments,
        'my_cart_count':my_cart_count,
        'my_ship_count':my_ship_count
    })

def add_add_to_cart(request, listing_id):
    user = request.user
    listing = ShoppingList.objects.get(pk = listing_id)
    listing.add_to_cart.add(user) 

    messages.success(request,"+Added to Cart Successfully!")
    """
    adding the user to the add_to_cart to reference the listing
    Whenever the user is loggged in all the list(add_to_cart) that link to it(user)
    will display to the add_to_cart page.
    because add_to_cart is using Many to many field 
    it can have multiple user and the user can have multiple add_to_cart
    """
    #after adding the listing to the add_to_cart it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def add_to_favorites(request, listing_id):
    user = request.user
    listing = ShoppingList.objects.get(pk = listing_id)
    listing.favorite.add(user) 

    messages.success(request,"Added to Favorites Successfully!")
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

    messages.success(request,"Removed Successfully!")
    """
    removing the link of the listing to the user.
    """
    #after removing the listing to the add_to_cart of the user it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def removed_to_favorites(request, listing_id):
    user = request.user
    listing = ShoppingList.objects.get(pk = listing_id)  
    listing.favorite.remove(user) 

    messages.success(request,"Removed Successfully!")
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
def view_profile(request,user_id):
    user = request.user
    my_cart_count = user.added_to_cart.all().count()
    my_ship_count = user.customerCheckoutOrder.all().count() 
    print(user)
    #fix UserProfile and delete it 
    userProfiles = User.objects.get(pk=user_id)
    listing = ShoppingList.objects.filter(owner = user)
    return render(request, "quanta/profile_page.html",{
        "listing":listing,
        'my_cart_count':my_cart_count,
        'userProfiles':userProfiles,
        'my_ship_count':my_ship_count
        })

def update_details(request, user_id):
    user = User.objects.get(pk=user_id)
    user_profile = User.objects.get(pk=user_id)
    if request.method == "POST":

        print(request.POST)

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        # if len(request.FILES) != 0:
        #     if len(user_profile.profile_img) > 0:
        #         os.remove(user_profile.profile_img.path)
        #     user_profile.profile_img = request.FILES['profile_img']
        user_profile.nationality = request.POST.get("nationality")
        user_profile.phone_no = request.POST.get("phone_no")
        user_profile.address = request.POST.get("address")
        user_profile.street_no = request.POST.get("street_no")
        user_profile.postal_code = request.POST.get("postal_code")
        user_profile.save()
        messages.success(request, "Profile Updated Successfully!")
        return HttpResponseRedirect(
            reverse('view_profile', args=(user_id, )))
    else:
        return HttpResponseRedirect(
            reverse('view_profile', args=(user_id, )))

def update_profile(request,user_id):
    user_profile = User.objects.get(pk=user_id)
    if request.method == "POST":
        user_profile.pictures = request.FILES.get("profile_img")
        user_profile.save()
        messages.success(request, "Profile Updated Successfully!")
        return HttpResponseRedirect(
            reverse('view_profile', args=(user_id, )))
    else:
        return HttpResponseRedirect(
            reverse('view_profile', args=(user_id, )))

def user_products(request):
    user = request.user
    print(user)
    my_cart_count = user.added_to_cart.all().count()
    my_ship_count = user.customerCheckoutOrder.all().count() 
    listing = ShoppingList.objects.filter(owner = user)
    return render(request, "quanta/my_products.html",{
        "listing":listing,
        'my_cart_count':my_cart_count,
        'my_ship_count':my_ship_count
    })
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


def add_to_cart(request,user_id): 
    user = request.user
    # items = ShoppingList.objects.get(pk = user_id)
    # total = user.added_to_cart.starting_price.count()
    subtotal = 0
    user_add_to_cart = user.added_to_cart.all()
    
    for active_listing in user_add_to_cart:
        print('items added to cart: ')
        print(active_listing)
        subtotal = subtotal + active_listing.starting_price
        
    total = 20 + subtotal
    my_cart_count = user.added_to_cart.all().count()
    my_ship_count = user.customerCheckoutOrder.all().count() 
    return render(request, "quanta/add_to_cart.html",{
        'user_add_to_cart': user_add_to_cart,
        'my_cart_count':my_cart_count,
        'subtotal':subtotal,
        'total':total,
        'my_ship_count':my_ship_count
    })

def checkout(request): 
    user = request.user
    # items = ShoppingList.objects.get(pk = user_id)
    # total = user.added_to_cart.starting_price.count()
    print('Total: ')
    subtotal = 0
    user_add_to_cart = user.added_to_cart.all()
    for active_listing in user_add_to_cart:
        subtotal = subtotal + active_listing.starting_price
    total = 20 + subtotal
    my_cart_count = user.added_to_cart.all().count()
    my_ship_count = user.customerCheckoutOrder.all().count() 
    return render(request, "quanta/checkout_page.html",{
        'user_add_to_cart': user_add_to_cart,
        'my_cart_count':my_cart_count,
        'subtotal':subtotal,
        'total':total,
        'my_ship_count':my_ship_count
    })

def finish(request):
    if request.method == "POST": 
        user = request.user
        mop = request.POST['mop']
        
        ordered = CheckoutOrder(customer = user, mop = mop)
        ordered.save()
        
        subtotal = 0
        user_add_to_cart = user.added_to_cart.all()
        for active_listing in user_add_to_cart:
            print("list: ",active_listing)
            ordered.product_ordered.add(active_listing)
            subtotal = subtotal + active_listing.starting_price
        total = 20 + subtotal
        my_ship_count = user.customerCheckoutOrder.all().count() 
        my_cart_count = user.added_to_cart.all().count()
        ordered_items = ordered.product_ordered.all()
        messages.success(request, "Ordered Successfully!")
        return render(request, "quanta/finish_page.html",{
            'user_add_to_cart': user_add_to_cart,
            'my_cart_count':my_cart_count,
            'subtotal':subtotal,
            'total':total,
            'ordered_items':ordered_items,
            'ordered': ordered,
            'my_ship_count':my_ship_count
        })

def ship_page(request):
    user = request.user
        
    ordered = CheckoutOrder.objects.filter(customer = user)
    my_ship_count = user.customerCheckoutOrder.all().count()   

    subtotal = 0
    user_add_to_cart = user.added_to_cart.all()
    for active_listing in user_add_to_cart:
        print("list: ",active_listing)
        subtotal = subtotal + active_listing.starting_price
    total = 20 + subtotal

    
    for order in ordered:
        items = order.product_ordered.all()
        print(items)
        for item in items:
            print('items', item)

    my_cart_count = user.added_to_cart.all().count()
    
    ordered_items = ordered.all()
    return render(request, "quanta/ship_page.html",{
        'user_add_to_cart': user_add_to_cart,
        'my_cart_count':my_cart_count,
        'subtotal':subtotal,
        'total':total,
        'ordered_items':ordered_items,
        'my_ship_count':my_ship_count
    })

def my_favorites(request): 
    user = request.user
    user_add_to_favorites = user.added_to_favorite.all()
    my_cart_count = user.added_to_cart.all().count()
    my_ship_count = user.customerCheckoutOrder.all().count() 
    return render(request, "quanta/add_to_favorites.html",{
        'user_add_to_favorites': user_add_to_favorites,
        'my_cart_count':my_cart_count,
        'my_ship_count':my_ship_count
    })

def payment_page(request):
    return render(request,"quanta/payment_page.html")
    
def createlist(request):
    user = request.user
    if user.is_authenticated:
        my_cart_count = user.added_to_cart.all().count()
        my_ship_count = user.customerCheckoutOrder.all().count() 
    else:
        my_cart_count = 0
    return render(request, "quanta/createlist.html",{
        'my_cart_count':my_cart_count,
        'my_ship_count':my_ship_count
    })


def all_list(request):
    all_listings = ShoppingList.objects.all()
    user = request.user
    if user.is_authenticated:
        my_cart_count = user.added_to_cart.all().count()
        my_ship_count = user.customerCheckoutOrder.all().count()   
    else:
        my_cart_count = 0
    return render(request, "quanta/all_list.html",{
        'all_listings': all_listings,
        'my_cart_count':my_cart_count,
        'my_ship_count': my_ship_count
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



