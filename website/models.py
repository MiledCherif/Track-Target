from django.db import models
from django.contrib.auth.models import User
from website.choices import REGIONS
from website.choices import STATUTS





class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_user2')
    last_message = models.ForeignKey('Message', null=True, blank=True, on_delete=models.SET_NULL, related_name='last_message')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation between {self.user1.username} and {self.user2.username}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.content}'




def my_titlecase(s):
    return s.title()





    
    



class Projet(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    membres = models.ManyToManyField(User, related_name='projets')
    progression = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
    





class Campagne(models.Model):
    nom = models.CharField(max_length=255)
    date = models.DateField()
    duree = models.DateField()
    region = models.CharField(max_length=255, choices=[(r, my_titlecase(r)) for r in REGIONS], blank=True, null=True)
    motif = models.CharField(max_length=255, blank=True, null=True)
    investissement = models.DecimalField(max_digits=10, decimal_places=2)
    domaine = models.CharField(max_length=255)
    user_asso = models.ForeignKey(User, on_delete=models.CASCADE)
    projet_asso = models.ForeignKey(Projet, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    tel2 = models.CharField(max_length=255, blank=True, null=True)
    domaine = models.CharField(max_length=255, blank=True, null=True)
    projet_client = models.CharField(max_length=255, blank=True, null=True)
    projet_asso = models.ForeignKey(Projet, on_delete=models.CASCADE, blank=True, null=True)
    user_asso = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=255, choices=[(r, my_titlecase(r)) for r in REGIONS], blank=True, null=True)

    def __str__(self):
        return self.nom

class Prospet(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    tel2 = models.CharField(max_length=255, blank=True, null=True)
    domaine = models.CharField(max_length=255, blank=True, null=True)
    projet_prospet = models.CharField(max_length=255, blank=True, null=True)
    projet_asso = models.ForeignKey(Projet, on_delete=models.CASCADE, blank=True, null=True)
    user_asso = models.ForeignKey(User, on_delete=models.CASCADE)    
    region = models.CharField(max_length=255, choices=[(r, my_titlecase(r)) for r in REGIONS], blank=True, null=True)
    
    def __str__(self):
        return self.nom
    
    
    
    
class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=255, choices=[(r, my_titlecase(r)) for r in STATUTS])
    user_asso = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.client.nom

# Create your models here.


class DashUsers(models.Model):
	email = models.EmailField('Email', max_length=100)
	username = models.CharField('Username', max_length=100)
	password = models.CharField('Password', max_length=100)
	birth_date = models.DateTimeField('Birth Date')
	def __str__(self):
		return self.email

class Projects(models.Model):
	Project_Name = models.CharField('Project_Name', max_length=100)
	description = models.TextField(blank=True)
	members = models.ManyToManyField(DashUsers, blank=True)
	def __str__(self):
		return self.Project_Name

