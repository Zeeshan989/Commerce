from django.contrib import admin
from .models import Listing,User,Bid,Winnerbid,CommentContent,Watchlist

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Winnerbid)
admin.site.register(CommentContent)
admin.site.register(Watchlist)




