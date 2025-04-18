from django.contrib import admin
from .models import DashUsers
from .models import Projet
from .models import Client
from .models import Prospet
from .models import Campagne
from .models import Conversation
from .models import Message
from .models import Transaction

# Register your models here.

admin.site.register(Conversation)
admin.site.register(Message)

admin.site.register(Projet)

admin.site.register(Client)
admin.site.register(Prospet)
admin.site.register(Campagne)
admin.site.register(Transaction)


admin.site.register(DashUsers)


