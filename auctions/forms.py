from django import forms

class kin(forms.Form):
    title = forms.CharField(max_length=65)
    description = forms.CharField(widget=forms.Textarea)
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    starting_bid = forms.IntegerField()
    image_url = forms.URLField(label='Image URL')

class ban(forms.Form):
    bn = forms.IntegerField()
   
class Comments(forms.Form):
    comments = forms.CharField(widget=forms.Textarea)