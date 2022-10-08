from django.db import models
from django.contrib.auth.models import User


#Model for apartment adverts
class Adverts (models.Model):
    Ad_Title = models.TextField()
    price_Title = models.TextField(default=None, blank=True)
    price = models.IntegerField()
    property_location = models.TextField()
    Address = models.TextField()
    category_choices = [
        ('RENT', 'Rent'),
        ('SALE', 'Sale'),
    ]
    listing_category = models.CharField(max_length=40, choices=category_choices, default='RENT')
    sq_ft = models.TextField()
    bed_rooms = models.TextField()
    bath_rooms = models.TextField()
    image = models.TextField(max_length=2083, default=None, blank=True)
    property_url = models.TextField(default=None, blank=True)
    picture = models.ImageField(upload_to='pictures/%y/%m/%d/', max_length=255, null=True, blank=True)
    lat = models.DecimalField(decimal_places=13, max_digits=21, default=None, blank=True)
    longi = models.DecimalField(max_digits=21, decimal_places=13, default=None, blank=True)
    bookmarked = models.ManyToManyField(User, related_name='bookmark', default=None, blank=True)


