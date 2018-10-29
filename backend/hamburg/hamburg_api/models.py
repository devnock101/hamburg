""" Models """

from django.db import models


class EmailAlertModel(models.Model):
    """Model for email alert"""
    email = models.TextField(null=False)
    movie_name = models.TextField(null=False)
    release_date = models.DateField(null=False)
    alert_date = models.DateField(null=True)
    done = models.BooleanField(default=False)

    class Meta:
        """Meta class for EmailAlertModel"""
        managed = False
        db_table = 'email_alert'


class MovieIdMapperModel(models.Model):
    """Model for internal id mapping between moviedb and movieglu"""
    moviedb_id = models.TextField(null=False)
    movieglu_id = models.TextField(null=False)
    imdb_id = models.TextField(null=False)

    class Meta:
        """Meta class for MovieIdMapperModel"""
        managed = False
        db_table = 'id_mapper'
