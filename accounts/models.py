from django.db import models

#MODEL FOR USER
class User(models.Model):
    user_id=models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)

#MODEL FOR STOK SYMBOL
class Symbol(models.Model):
    sid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

#MODEL FOR SYMBOLS OF A USER (MANY-TO-MANY RELATIONSHIP)
class UserSymbol(models.Model):
    u_s_id=models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    User_symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)