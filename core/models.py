from django.db import models
from decouple import config

class Benefit(models.Model):
    venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='venueId')  # Field name made lowercase.
    title = models.TextField()
    recurrence = models.TextField()

    class Meta:
        managed = config("DB_MANAGED", False, cast=bool)
        db_table = 'benefit'


class BenefitUsage(models.Model):
    personid = models.ForeignKey('Person', models.DO_NOTHING, db_column='personId')  # Field name made lowercase.
    benefitid = models.ForeignKey(Benefit, models.DO_NOTHING, db_column='benefitId')  # Field name made lowercase.
    usagetimestamp = models.DateTimeField(db_column='usageTimestamp')  # Field name made lowercase.

    class Meta:
        managed = config("DB_MANAGED", False, cast=bool)
        db_table = 'benefit_usage'


class Person(models.Model):
    name = models.TextField()

    class Meta:
        managed = config("DB_MANAGED", False, cast=bool)
        db_table = 'person'


class Venue(models.Model):
    name = models.TextField()

    class Meta:
        managed = config("DB_MANAGED", False, cast=bool)
        db_table = 'venue'
