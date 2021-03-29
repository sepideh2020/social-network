from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Relationship


@receiver(post_save, sender=Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
    """is used for adding friends automatically"""
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.id)
        receiver_.friends.add(sender_.id)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)  # signal is pre_delete and receiver is Relationship
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    """before the relationship get deleted,it is removed from friends"""
    # here sender is instance of Relationship
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.id)
    receiver.friends.remove(sender.id)
    sender.save()
    receiver.save()
