from django.db import models
from django.contrib.auth.models import User, Group


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_to_user(self):
        return self.to_user

    @classmethod
    def create_friend(cls, from_user, to_user):
        friend = cls(from_user=from_user, to_user=to_user)
        friend.save()
        return friend




def get_default_profile_image_url():
    return '/media/default_images/avatar.jpg'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default=get_default_profile_image_url)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='friends')

    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return get_default_profile_image_url()

