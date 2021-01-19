from django.db import models

# Create your models here.

class things(models.TextChoices):
    EDU = 'e',"教育"
    LIF = 'l',"生活"
    MED = 'm',"医疗"
    SAL = 's',"工资"



class user(models.Model):
    name = models.CharField(max_length=25)
    passwd = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    has_confirmed = models.BooleanField(default=False)

class mylog(models.Model):
    userID = models.ForeignKey(user,on_delete=models.CASCADE)
    operator = models.CharField(max_length=255,blank=True)

class income(models.Model):
    detail = models.CharField(verbose_name="详细事件",max_length=255)
    userID = models.ForeignKey(user,on_delete=models.CASCADE)
    inmoney = models.IntegerField(verbose_name="收入金额")
    things = models.CharField(verbose_name="收入种类", max_length=1, choices=things.choices)
    data = models.DateField(auto_now_add=True)

class outcome(models.Model):
    detail = models.CharField(verbose_name="详细事件",max_length=255)
    userID = models.ForeignKey(user,on_delete=models.CASCADE)
    outmoney = models.IntegerField(verbose_name="支出金额")
    things = models.CharField(verbose_name="支出种类", max_length=1, choices=things.choices)
    data = models.DateField(auto_now_add=True)

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('user', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
