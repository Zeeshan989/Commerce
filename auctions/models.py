from django.contrib.auth.models import AbstractUser
from django.db import models



class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=65)
    title = models.CharField(max_length=65)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)
    l_uid=models.CharField(max_length=65,default='')
    closed=models.CharField(max_length=65,default='')
    

class User(AbstractUser):
    pass 

class Bid(models.Model):
    bd=models.IntegerField()
    biduid=models.CharField(max_length=65)
    bpid=models.IntegerField()

class Winnerbid(models.Model):
    pid=models.IntegerField(default=0)
    winner=models.CharField(max_length=65,default='temp')

class CommentContent(models.Model):
    userc=models.CharField(max_length=65,default='temp2')
    prid=models.IntegerField(default=0)
    ct=models.CharField(max_length=65,default='temp')

class Watchlist(models.Model):
    userw=models.CharField(max_length=65,default='temp2')
    prwd=models.IntegerField(default=0)
    wt = models.CharField(max_length=65,default='')
    il = models.URLField(blank=True,default='')


    
    



  

     
   
    

