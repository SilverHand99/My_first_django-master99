from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from my_projekt.models import User_Profile, Car_Complekt, Car, Cart, CartContent


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


def create_kit(instance, **kwargs):
    if kwargs["action"] == 'post_add':
        if instance.items.count() < 2:
            raise ValidationError(f'You cant assign less than two regions, now {instance.items.count()}')
    total = 0
    for item in instance.items.all():
        total += item.price
    instance.total_before = total
    instance.total_after = (total * (100 - instance.sell) / 100)
    #instance.sell = (100 - (instance.total_after / (total / 100)))
    instance.save()


m2m_changed.connect(create_kit, sender=Car_Complekt.items.through)


# def create_car(instance, created, **kwargs):
#     total = 0
#     # for category in instance.categories.all():
#     #     total = category.get(id=1)
#     instance.categories = total
#     instance.save()


#m2m_changed.connect(create_car, sender=Car.categories.through)


# @receiver(post_save, sender=User)
# def content_save(instance, created, self, **kwargs, ):
#     session_key = self.request.session.session_key
#     cart_content = CartContent.objekts.filter()
#     if created:
#         CartContent.objects.filter(cart__session_key=instance)
