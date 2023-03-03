from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(_("Name"),max_length=100)
    date_created = models.DateTimeField(_("Date Created"),default=now)

    class Meta:
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f'{self.name}'
    

class Conversation(models.Model):
    user = models.ForeignKey(User,verbose_name=_("User"),on_delete=models.SET_NULL,null=True,blank=True)
    msg = models.TextField()
    date_created = models.DateTimeField(_("Date Created"),default=now)
    user_ip = models.CharField(_("User IP"),max_length=50)
    user_device = models.CharField(_("Device"),max_length=255)

    class Meta:
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        return f'{self.user} - {self.msg}'