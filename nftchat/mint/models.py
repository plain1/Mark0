from django.db import models

class Register(models.Model):
    nft_name = models.CharField(max_length=100)
    nft_image = models.ImageField(blank = True)

    Token_uri = models.TextField()
    Token_id = models.TextField()
    
    room_name = models.CharField(max_length=200)
    nft_price = models.IntegerField()
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nft_name

 

class Shopping(models.Model):
    nft_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=20)
    nft_price = models.IntegerField()
    shopped_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nft_name

