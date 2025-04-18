from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse

from dashtrack.settings import BASE_DIR
from .models import DashUsers
from .forms import UserForm
from django.contrib.auth.models import Group


from django.contrib.auth.decorators import login_required
from .forms import ProjetForm
from .forms import ClientForm
from .forms import ProspetForm
from .forms import CampagneForm
from .forms import TransactionForm
from .forms import UpdateTransactionForm
from .models import Projet
from .models import Client
from .models import Prospet
from .models import Campagne
from .models import Transaction
from members.models import Friend
from members.models import Profile
from django.urls import reverse
from members.views import friends_list
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Conversation, Message
from .forms import MessageForm
from django.db.models import Q

from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from django.shortcuts import render
from django.db.models import Sum
from .models import Transaction, Client
from django.db.models import Count

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import Sum, Count, Q

import os
import time

from django .core.paginator import Paginator


def dashboard(request: HttpRequest, client_id=None) -> HttpResponse:
    
    # Calculer les ventes totales
    total_sales = Transaction.objects.filter(
        Q(client__user_asso=request.user) |
        Q(client__user_asso__in=request.user.profile.friends.all())
    ).aggregate(Sum('montant'))['montant__sum'] or 0

    # Calculer le nombre de transactions
    transactions_count = Transaction.objects.filter(
        Q(client__user_asso=request.user) |
        Q(client__user_asso__in=request.user.profile.friends.all())
    ).count()
    
    # récupérer les statistiques de la semaine
    start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    weekly_stats = Transaction.objects.filter(
        Q(client__user_asso=request.user) |
        Q(client__user_asso__in=request.user.profile.friends.all()),
        date__range=[start_of_week, end_of_week]
    )
    
    # calculer le montant total des ventes de la semaine
    total_weekly_sales = weekly_stats.aggregate(Sum('montant'))['montant__sum'] or 0
    
    # Calculer les statistiques du mois
    current_month = timezone.now().date().month
    start_of_month = timezone.datetime(timezone.now().year, current_month, 1).date()
    if current_month == 12:
        end_of_month = timezone.datetime(timezone.now().year + 1, 1, 1).date() - timezone.timedelta(days=1)
    else:
        end_of_month = timezone.datetime(timezone.now().year, current_month + 1, 1).date() - timezone.timedelta(days=1)

    monthly_stats = Transaction.objects.filter(
        Q(client__user_asso=request.user) |
        Q(client__user_asso__in=request.user.profile.friends.all()),
        date__range=[start_of_month, end_of_month]
        )

    # Calculer le montant total des ventes du mois
    total_monthly_sales = monthly_stats.aggregate(Sum('montant'))['montant__sum'] or 0
    
    # Calculer les investissements totaux
    total_investments = Campagne.objects.filter(projet_asso__membres=request.user).aggregate(Sum('investissement'))['investissement__sum'] or 0
    total_investments = round(total_investments, 2)  # Arrondir à deux décimales
    
    # calculer la variation en pourcentage par rapport à la semaine précédente
    last_week_start = start_of_week - timezone.timedelta(days=7)
    last_week_end = end_of_week - timezone.timedelta(days=7)
    last_week_stats = Transaction.objects.filter(
        Q(client__user_asso=request.user) |
        Q(client__user_asso__in=request.user.profile.friends.all()),
        date__range=[last_week_start, last_week_end]
        )
    last_week_sales = last_week_stats.aggregate(Sum('montant'))['montant__sum'] or 0
    week_percent_change = ((total_weekly_sales - last_week_sales) / last_week_sales) * 100 if last_week_sales else 100

    # calculer la variation en pourcentage par rapport à la semaine avant la dernière
    before_last_week_start = last_week_start - timezone.timedelta(days=7)
    before_last_week_end = last_week_end - timezone.timedelta(days=7)
    before_last_week_stats = Transaction.objects.filter(date__range=[before_last_week_start, before_last_week_end])
    before_last_week_sales = before_last_week_stats.aggregate(Sum('montant'))['montant__sum'] or 0
    last_week_percent_change = ((last_week_sales - before_last_week_sales) / before_last_week_sales) * 100 if before_last_week_sales else 100
    
    # Récupérer les données pour les graphiques de la semaine
    weekly_sales_data = Transaction.objects.filter(
        Q(client__user_asso=request.user) | Q(client__user_asso__in=request.user.profile.friends.all())
    ).values('date').annotate(total_sales=Sum('montant')).order_by('date')

    weekly_dates = [data['date'].strftime('%Y-%m-%d') for data in weekly_sales_data]
    weekly_totals = [data['total_sales'] for data in weekly_sales_data]
    
    # Création du premier graphique : ventes hebdomadaires
    fig1, ax1 = plt.subplots()
    ax1.plot(weekly_dates, weekly_totals)
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Ventes hebdomadaires')
    ax1.set_title('Ventes hebdomadaires')
    ax1.grid(True)
    ax1.set_xticklabels(weekly_dates, rotation=45)
    fig1.tight_layout()

    # Enregistrer le premier graphique dans un fichier
    timestamp = int(time.time())
    weekly_chart_path = os.path.join(BASE_DIR, 'static/website/charts', f'graphique_{timestamp}.png')
    fig1.savefig(weekly_chart_path)
    
    # Récupération des régions et du nombre de clients
    regions_clients = Client.objects.filter(
        Q(user_asso=request.user) | Q(user_asso__in=request.user.profile.friends.all())
    ).values('region').annotate(total_clients=Count('id'))

    # Trie des régions en fonction du nombre de clients (ordre décroissant)
    regions_clients = sorted(regions_clients, key=lambda x: x['total_clients'], reverse=True)

    # Nombre maximum de régions à afficher dans le graphique
    N = 5

    # Sélection des N premières régions avec le plus de clients
    top_regions = [r['region'] for r in regions_clients[:N]]
    top_clients = [r['total_clients'] for r in regions_clients[:N]]
    
    # Création du deuxième graphique : répartition des clients par région
    fig2, ax2 = plt.subplots()
    ax2.pie(top_clients, labels=top_regions, autopct='%1.1f%%')
    ax2.set_title('Répartition des clients par région (Top {})'.format(N))

    # Enregistrer le deuxième graphique dans un fichier
    region_chart_path = os.path.join(BASE_DIR, 'static/website/charts', f'pie_{timestamp}.png')
    fig2.savefig(region_chart_path)
    
    # Fermer les figures pour libérer la mémoire
    plt.close(fig1)
    plt.close(fig2)
    
    # Création du graphique des campagnes classées par investissement
    campaigns = Campagne.objects.filter(projet_asso__membres=request.user).order_by('-investissement')
    campaign_names = [campaign.nom for campaign in campaigns]
    investments = [campaign.investissement for campaign in campaigns]

    fig3, ax3 = plt.subplots()
    ax3.bar(campaign_names, investments)
    ax3.set_xlabel("Campagne")
    ax3.set_ylabel("Investissement")
    ax3.set_title("Investissement par campagne")
    ax3.tick_params(axis='x', rotation=90)  # Rotation des étiquettes sur l'axe des x pour une meilleure lisibilité
    fig3.tight_layout()

    # Enregistrer le graphique des campagnes dans un fichier
    campaign_chart_path = os.path.join(BASE_DIR, 'static/website/charts', f'campaign_chart_{timestamp}.png')
    fig3.savefig(campaign_chart_path)

    # Fermer la figure pour libérer la mémoire
    plt.close(fig3)
   
    # calculer les clients
    clients = Client.objects.annotate(total_transactions=Sum('transaction__montant'))

    clients_count = Client.objects.filter(
        Q(user_asso=request.user) | Q(user_asso__in=request.user.profile.friends.all())
    ).count()
    
    if client_id is None:
        client = Client.objects.all()
    else:
        client = get_object_or_404(Client, id=client_id)
    
    # Récupérer les projets
    projets = Projet.objects.filter(
        Q(membres=request.user) | Q(createur=request.user)
    ).distinct()
    
    
    # Recuperer les transaction en attente
    transactions_en_attente = Transaction.objects.filter(statut="En Attente")
    noms_clients = [transaction.client.nom for transaction in transactions_en_attente]
    
    
    
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    
    
    
    context = {
        'total_sales': total_sales,
        'transactions_count': transactions_count,
        'total_weekly_sales': total_weekly_sales,
        'total_investments': total_investments,
        'week_percent_change': week_percent_change,
        'last_week_percent_change': last_week_percent_change,
        
        'weekly_dates': weekly_dates,
        'weekly_totals': weekly_totals,
        'total_monthly_sales': total_monthly_sales,
        
        'weekly_chart_filename': f'graphique_{timestamp}.png',
        'region_chart_filename': f'pie_{timestamp}.png',
        'campaign_chart_filename': f'campaign_chart_{timestamp}.png',
        
        'clients_count': clients_count,
        'friends': friends,
        'clients':clients,
        'projets': projets,
        'transactions_en_attente': transactions_en_attente,
        'noms_clients': noms_clients,
        
    }
    return render(request, 'dashboard.html', context)













def dashboard2d(request: HttpRequest, user_id=None) -> HttpResponse:
    if user_id is None:
        friend = Friend.objects.all()
    else:
        friend = get_object_or_404(Friend, id=user_id)
    return render(request, 'dashboard.html', {'friends': friend})






@login_required
def conversations(request):
    profile = request.user.profile
    friends = profile.friends.all()
    conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)
    return render(request, 'messages.html', {'conversations': conversations, 'friends': friends})

@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    
    conversation = Conversation.objects.filter(
        Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(user1=request.user, user2=other_user, last_message=None)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.last_message = message
            conversation.save()
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm(initial={'receiver': other_user})

    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'conversation.html', {'other_user': other_user, 'messages': messages, 'form': form, 'friend_username': other_user.username, 'friend_id': other_user.id})



@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            other_user = get_object_or_404(User, pk=user_id)
            conversation = Conversation.objects.filter(user1=request.user, user2=other_user).first() or Conversation.objects.filter(user1=other_user, user2=request.user).first()
            if not conversation:
                conversation = Conversation.objects.create(user1=request.user, user2=other_user, last_message=None)
            message = form.save(commit=False)
            message.sender = request.user
            if other_user:
                message.receiver_id = other_user.id
            message.conversation = conversation
            message.save()
            conversation.last_message = message
            conversation.save()
            return redirect(reverse('conversation', args=[user_id]))
        else:
            messages = list(form.errors.values())
            return JsonResponse({'status': 'error', 'messages': messages})
    else:
        return redirect(reverse('conversation', args=[user_id]))






@login_required
def friends_list(request: HttpRequest, user_id=None) -> HttpResponse:
    if user_id is None:
        friend = Friend.objects.all()
    else:
        friend = get_object_or_404(Friend, id=user_id)
    filters = request.GET.keys()
    print(filters)
    filtersValue = request.GET.items()
    print(filtersValue)
    return render(request, 'members/friends_list.html', {'friends': friend})


def prospet_fiche(request, prospet_id):
    prospet = Prospet.objects.get(id=prospet_id)
    context = {'prospet': prospet}
    return render(request, 'prospet_fiche.html', context)

def projet_fiche(request, projet_id):
    projet = Projet.objects.get(id=projet_id)
    context = {'projet': projet}
    return render(request, 'projet_fiche.html', context)

def client_fiche(request, client_id):
    client = Client.objects.get(id=client_id)
    context = {'client': client}
    return render(request, 'client_fiche.html', context)

def campagne_fiche(request, campagne_id):
    campagne = Campagne.objects.get(id=campagne_id)
    context = {'campagne': campagne}
    return render(request, 'campagne_fiche.html', context)


def update_projet(request, projet_id):
    projet = Projet.objects.get(pk=projet_id)
    form = ProjetForm(request.POST or None, instance=projet)
    if form.is_valid():
        form.save()
        return redirect(reverse('projet-fiche', args=[projet.id]))
    return render(request, 'update_projet.html', {'projet': projet, 'form':form})


def update_campagne(request, campagne_id):
    campagne = Campagne.objects.get(pk=campagne_id)
    form = CampagneForm(request.POST or None, instance=campagne)
    if form.is_valid():
        form.save()
        return redirect(reverse('campagne-fiche', args=[campagne.id]))
    return render(request, 'update_campagne.html', {'campagne': campagne, 'form':form})


def update_prospet(request, prospet_id):
    prospet = Prospet.objects.get(pk=prospet_id)
    form = ProspetForm(request.POST or None, instance=prospet)
    if form.is_valid():
        form.save()
        return redirect(reverse('prospet-fiche', args=[prospet.id]))
    return render(request, 'update_prospet.html', {'prospet': prospet, 'form':form})

def update_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect(reverse('client-fiche', args=[client.id]))
    return render(request, 'update_client.html', {'client': client, 'form':form})


def update_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    form = UpdateTransactionForm(request.POST or None, instance=transaction)
    if form.is_valid():
        form.save()
        return redirect(reverse('transactions'))
    return render(request, 'update_transaction.html', {'transaction': transaction, 'form':form})




def delete_conversation(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    conversation.delete()
    return redirect(reverse('conversations'))

def delete_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    message.delete()
    return redirect('conversations')

def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    return redirect('transactions')

def delete_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    client.delete()
    return redirect('clients')

def delete_prospet(request, prospet_id):
    prospet = Prospet.objects.get(pk=prospet_id)
    prospet.delete()
    return redirect('prospets')

def delete_campagne(request, campagne_id):
    campagne = Campagne.objects.get(pk=campagne_id)
    campagne.delete()
    return redirect('campagnes')

def delete_projet(request, projet_id):
    projet = Projet.objects.get(pk=projet_id)
    projet.delete()
    return redirect('projets')

@login_required
def creer_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user_asso = request.user
            client.save()
            return redirect(reverse('clients'))
    else:
        form = ClientForm()
    return render(request, 'creer-client.html', {'form': form})

@login_required
def creer_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user_asso = request.user
            transaction.save()
            return redirect(reverse('transactions'))
    else:
        form = TransactionForm()
    return render(request, 'creer-transaction.html', {'form': form})



@login_required
def creer_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.createur = request.user
            projet.save()
            projet.membres.add(request.user)
            return redirect(reverse('projets'))
    else:
        form = ProjetForm()
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    return render(request, 'creer-projet.html', {'form': form, 'friends': friends})



def projets(request: HttpRequest, projet_id=None) -> HttpResponse:
    p = Paginator(Projet.objects.all(), 6)
    page = request.GET.get('page')
    query = request.GET.get('q')
    if projet_id is None:
        if query:
            projet = Projet.objects.filter(nom__icontains=query)
        else:
            projet = p.get_page(page)
    else:
        projet = get_object_or_404(Projet, id=projet_id)
        
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    
    return render(request, 'projets.html', {'projets': projet, 'friends': friends})




def clients(request: HttpRequest, client_id=None) -> HttpResponse:
    p = Paginator(Client.objects.all(), 8)
    page = request.GET.get('page')
    query = request.GET.get('q')

    if client_id is None:
        if query:
            client = Client.objects.filter(nom__icontains=query)
        else:
            client = p.get_page(page)
    else:
        client = get_object_or_404(Client, id=client_id)
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    return render(request, 'clients.html', {'clients': client, 'friends': friends})





def transactions(request: HttpRequest, transaction_id=None) -> HttpResponse:
    p = Paginator(Transaction.objects.all(), 10)
    page = request.GET.get('page')
    query = request.GET.get('q')
    if transaction_id is None:
        if query:
            transaction = Transaction.objects.filter(client__nom__icontains=query)
        else:
            transaction = p.get_page(page)
    else:
        transaction = get_object_or_404(Transaction, id=transaction_id)
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    return render(request, 'transactions.html', {'transactions': transaction, 'friends': friends})




def prospets(request: HttpRequest, prospet_id=None) -> HttpResponse:
    p = Paginator(Prospet.objects.all(), 8)
    page = request.GET.get('page')
    query = request.GET.get('q')
    if prospet_id is None:
        if query:
            prospet = Prospet.objects.filter(nom__icontains=query)
        else:
            prospet = p.get_page(page)
    else:
        prospet = get_object_or_404(Prospet, id=prospet_id)
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    return render(request, 'prospets.html', {'prospets': prospet, 'friends': friends})

def campagnes(request: HttpRequest, campagne_id=None) -> HttpResponse:
    p = Paginator(Campagne.objects.all(), 8)
    page = request.GET.get('page')
    if campagne_id is None:
        campagne = p.get_page(page)
    else:
        campagne = get_object_or_404(Campagne, id=campagne_id)
    filters = request.GET.keys()
    print(filters)
    filtersValue = request.GET.items()
    print(filtersValue)
    # les amis 
    profile = request.user.profile
    friends = profile.friends.all()
    return render(request, 'campagnes.html', {'campagnes': campagne, 'friends': friends})






def rapport_roi(request, campagne_id):
    campagne = Campagne.objects.get(id=campagne_id)
    transactions = Transaction.objects.filter(projet=campagne.projet_asso, date__gte=campagne.date, date__lte=campagne.date + timedelta(days=campagne.duree.day))
    montant_total = transactions.aggregate(Sum('montant'))['montant__sum'] or 0
    roi = (montant_total - campagne.investissement) / campagne.investissement * 100 if campagne.investissement != 0 else 0
    data = {
        'nom_campagne': campagne.nom,
        'id_campagne': campagne.id,
        'montant_investi': campagne.investissement,
        'montant_total': montant_total,
        'roi': roi,
    }
    return render(request, 'rapport_roi.html', {'data': data})








@login_required
def creer_prospet(request):
    if request.method == 'POST':
        form = ProspetForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user_asso = request.user
            client.save()
            return redirect(reverse('prospets'))
    else:
        form = ProspetForm()
    return render(request, 'creer-prospet.html', {'form': form})


@login_required
def creer_campagne(request):
    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.user_asso = request.user
            campagne.save()
            return redirect(reverse('campagnes'))
    else:
        form = CampagneForm()
    return render(request, 'creer-campagne.html', {'form': form})




def home(request):
    return render(request, 'home.html', {})


def signin(request):
    return render(request, 'page-sign-in.html', {})


def lock(request):
    return render(request, 'page-lock.html', {})


def signup(request):
    submitted = False
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/signup?submitted=True')
    else:
        form = UserForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'page-sign-up.html', {'form': form, 'submitted': submitted})







def settings(request):
    return render(request, 'settings.html', {})



def map(request: HttpRequest, client_id=None) -> HttpResponse:
    if client_id is None:
        client = Client.objects.all()
    else:
        client = get_object_or_404(Client, id=client_id)
    filters = request.GET.keys()
    print(filters)
    filtersValue = request.GET.items()
    print(filtersValue)
    return render(request, 'map.html', {'clients': client})



