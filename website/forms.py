from django import forms
from django.forms import ModelForm
from .models import DashUsers
from .models import Projet
from .models import Client
from .models import Prospet
from .models import Campagne
from .choices import REGIONS
from .choices import STATUTS
from .models import my_titlecase
from .models import Message
from .models import Transaction
from django.contrib.auth.models import User
from django.forms.widgets import DateInput
from django.forms import DateInput


class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=500, required=True)

    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
        if receiver:
            self.instance.receiver = receiver


class CustomDateInput(DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'  # Format de date personnalisé

class UpdateTransactionForm(forms.ModelForm):
    
    date = forms.DateField(widget=CustomDateInput(attrs={'class': 'form-control'}))
    montant = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    statut = forms.ChoiceField(choices=[(r, my_titlecase(r)) for r in STATUTS], widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Transaction
        fields = ['statut', 'montant','date']
        
        
        
        

    
    
class TransactionForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    projet = forms.ModelChoiceField(queryset=Projet.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    date = forms.DateField(widget=CustomDateInput(attrs={'class': 'form-control'}))
    montant = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    statut = forms.ChoiceField(choices=[(r, my_titlecase(r)) for r in STATUTS], widget=forms.Select(attrs={'class':'form-control'}))
    user_asso = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Transaction
        fields = ['client', 'projet', 'date', 'montant', 'statut', 'user_asso']

class ProjetForm(forms.ModelForm):
    nom = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    createur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    membres = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    progression = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))  # Champ de progression

    class Meta:
        model = Projet
        fields = ['nom', 'description', 'createur', 'membres', 'progression'] 


class CampagneForm(forms.ModelForm):
    nom = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(widget=CustomDateInput(attrs={'class': 'form-control'}))
    duree = forms.DateField(widget=CustomDateInput(attrs={'class': 'form-control'}))
    region = forms.ChoiceField(choices=[(r, my_titlecase(r)) for r in REGIONS], widget=forms.Select(attrs={'class':'form-control'}))
    motif = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    investissement = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    domaine = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    projet_asso = forms.ModelChoiceField(queryset=Projet.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Campagne
        fields = ['nom', 'date', 'duree', 'region', 'motif', 'investissement', 'domaine', 'projet_asso']


class ClientForm(forms.ModelForm):
    nom = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    adresse = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    domaine = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    projet_client = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    projet_asso = forms.ModelChoiceField(required=False, queryset=Projet.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    user_asso = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    region = forms.ChoiceField(choices=[(r, my_titlecase(r)) for r in REGIONS], widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Client
        fields = ['nom', 'adresse', 'tel', 'tel2', 'domaine', 'projet_client', 'projet_asso', 'user_asso', 'region']

class ProspetForm(forms.ModelForm):
    nom = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    domaine = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    projet_prospet = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    projet_asso = forms.ModelChoiceField(required=False, queryset=Projet.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    user_asso = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    region = forms.ChoiceField(choices=[(r, my_titlecase(r)) for r in REGIONS], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Prospet
        fields = ['nom', 'adresse', 'tel', 'tel2', 'domaine', 'projet_prospet', 'projet_asso', 'user_asso', 'region']

    def __init__(self, *args, **kwargs):
        super(ProspetForm, self).__init__(*args, **kwargs)
        self.fields['nom'].label = 'Nom'
        self.fields['adresse'].label = 'Adresse'
        self.fields['tel'].label = 'Téléphone'
        self.fields['tel2'].label = 'Téléphone 2'
        self.fields['domaine'].label = 'Domaine'
        self.fields['projet_prospet'].label = 'Entreprise du prospet'
        self.fields['projet_asso'].label = 'Projet Associé'
        self.fields['user_asso'].label = 'User Associé'
        self.fields['region'].label = 'Région'





class UserForm(ModelForm):
	class Meta:
		model = DashUsers
		fields = ('email', 'username', 'birth_date', 'password')