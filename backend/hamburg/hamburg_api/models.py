""" Models """

from django.db import models


class WelcomeModel(models.Model):
    wId = models.IntegerField(db_column='wId', primary_key=True)
    wText = models.TextField(db_column='wText')
    class Meta:
        managed = False
        db_table = 'welcome'
