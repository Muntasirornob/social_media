from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver 
from .models import Profile,Relationship

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
	print('sender',sender)
	print(instance)
	if created:
		Profile.objects.create(user=instance)
@receiver(post_save,sender=Relationship)
def post_save_friend_list(sender,instance,created,**kwargs):
	sender_friend=instance.sender
	receiver_friend=instance.receiver
	if instance.status=='accepted':
		sender_friend.friends.add(receiver_friend.user)
		receiver_friend.friends.add(sender_friend.user)
		sender_friend.save()
		receiver_friend.save()
@receiver(pre_delete,sender=Relationship)
def pre_delete_friends(sender,instance,**kwargs):
	sender=instance.sender
	receiver=instance.receiver
	sender.friends.remove(receiver.user)
	receiver.friends.remove(sender.user)
	sender.save()
	receiver.save()
