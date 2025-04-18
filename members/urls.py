from django.urls import path
from . import views	
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('profile/', views.profile, name='profile'),
    
    
    
    path('users_list/', views.users_list, name='users_list'),
    path('friends_list/', views.friends_list, name='friends_list'),
    
    path('add-friend/<int:selected_user_id>/', views.add_friend, name='add_friend'),
    path('delete_friend/<int:selected_user_id>/', views.delete_friend, name='delete_friend'),

    
    path('settings.html', views.settings, name="settings"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
