from email.headerregistry import Address
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.query_utils import select_related_descend


#AbstractUser automatic creating model and add some fields for the User
# Ex. username, password, email, firstname,lastname and etc.
class User(AbstractUser):
    phone_no = models.CharField(max_length=200, null=True)
    nationality= models.CharField(max_length=200, null=True)
    address =  models.CharField(max_length=200, null=True)
    pictures = models.ImageField(null=True, blank = True, upload_to = "profile/")
    street_no =  models.CharField(max_length=200, null=True)
    postal_code =  models.CharField(max_length=200, null=True)

        
class ShoppingList(models.Model):
    #default = None means that it will store none if the user decides not to fill the data.
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="shoppinglist",default=None)
    item_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    product_img = models.ImageField(null=True, blank = True, upload_to = "products/")
    starting_price = models.DecimalField( max_digits = 8, decimal_places=2 )
    category = models.CharField(max_length=20)
    #blank = true / basically it accepts even it is blank or empty it simple means it is not required
    add_to_cart = models.ManyToManyField(User, blank=True, related_name="added_to_cart")
    favorite = models.ManyToManyField(User, blank=True, related_name="added_to_favorite")
    #orders from all users
    orders = models.ManyToManyField(User, blank=True, related_name="added_to_orders")
    #using BooleanField to know if the listings is close or not/ sold
    is_closed = models.BooleanField(default=False, null=True,blank= True)
    #auto_now_add = a start date you first add a listings
    created_at = models.DateTimeField(auto_now_add=True)
    #auto_now = the date when you modifed/update a listings
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} : {self.item_name}"

class CheckoutOrder(models.Model):
    checkout_id = models.CharField(max_length=20)
    #cutomer ordered
    customer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="customerCheckoutOrder")
    #mode of payment
    mop = models.CharField(max_length=20)
    #product ordered Shoppinglist
    product_ordered = models.ManyToManyField(ShoppingList, blank=True, related_name="productsCheckoutOrder")
    #time when the ordered was add
    ordered_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} : {self.mop}"

class Comments(models.Model):
    #commentor is basically the user that logged in it is link to the User model/table
    commentor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments")
    #listing is the listings in Shoppinglist
    listings = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="comments")
    #text is the comments/message of the commentor/user.
    text = models.CharField(max_length=600)
    #time when the comment was add
    comment_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commentor.username} : {self.text}"