from django.urls import path, include
from . import views	
from .views import creer_projet
from .views import creer_client
from django.conf.urls.static import static
from django.conf import settings
from members.views import friends_list

urlpatterns = [
    
    path('home.html', views.home, name="home"),
    path('messages.html', views.conversations, name='conversations'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    
    
    
    
    
    
    path('page-sign-in.html', views.signin, name="signin"),
    path('page-sign-up.html', views.signup, name="signup"),
    path('page-lock.html', views.lock, name="lock"),
    path('signup/', views.signup, name='signup'),
    path('dashboard.html', views.dashboard, name="dashboard"),
    path('page-sign-in.html', views.signin, name="logout"),
    path('transactions.html', views.transactions, name="transactions"),
    path('settings.html', views.settings, name="settings"),
    path('map.html', views.map, name="map"),
    
    path('creer-projet.html', views.creer_projet, name='creer_projet'),
    path('creer-client.html', views.creer_client, name='creer_client'),
    path('creer-prospet.html', views.creer_prospet, name='creer_prospet'),
    path('creer-campagne.html', views.creer_campagne, name='creer_campagne'),
    path('creer-transaction.html', views.creer_transaction, name='creer_transaction'),
    
    path('creer-client/<int:projet_id>/', views.creer_client, name='creer_client'),
    
    path('projets/<int:projet_id>/', views.projets, name='projets'),
    path('clients/<int:client_id>/', views.clients, name='clients'),
    
    
    path('projets.html', views.projets, name='projets'),
    path('clients.html', views.clients, name='clients'),
    path('prospets.html', views.prospets, name='prospets'),
    path('campagnes.html', views.campagnes, name='campagnes'),
    
    path('update_client/<client_id>/', views.update_client, name='update-client'),
    path('update_projet/<projet_id>/', views.update_projet, name='update-projet'),
    path('update_prospet/<prospet_id>/', views.update_prospet, name='update-prospet'),
    path('update_campagne/<campagne_id>/', views.update_campagne, name='update-campagne'),
    path('update_transaction/<transaction_id>/', views.update_transaction, name='update-transaction'),
    
    path('delete_client/<client_id>/', views.delete_client, name='delete-client'),
    path('delete_prospet/<prospet_id>/', views.delete_prospet, name='delete-prospet'),
    path('delete_campagne/<campagne_id>/', views.delete_campagne, name='delete-campagne'),
    path('delete_projet/<projet_id>/', views.delete_projet, name='delete-projet'),
    path('delete_transaction/<transaction_id>/', views.delete_transaction, name='delete-transaction'),
    path('delete_message/<message_id>/', views.delete_message, name='delete-message'),
    path('delete_conversation/<conversation_id>', views.delete_conversation, name='delete-conversation'),
    
    path('client-fiche/<int:client_id>/', views.client_fiche, name='client-fiche'),
    path('projet-fiche/<int:projet_id>/', views.projet_fiche, name='projet-fiche'),
    path('prospet-fiche/<int:prospet_id>/', views.prospet_fiche, name='prospet-fiche'),
    path('campagne-fiche/<int:campagne_id>/', views.campagne_fiche, name='campagne-fiche'),
    path('rapport-roi/<int:campagne_id>/', views.rapport_roi, name='rapport-roi'),
    
    
    
    path('members/', include('members.urls')),
    
    
    

    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)