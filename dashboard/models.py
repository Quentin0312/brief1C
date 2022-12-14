from django.db import models

# Create your models here.

class Factures(models.Model):
    nofacture = models.CharField(max_length = 50, primary_key=True)
    datefacturation = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factures'

class Produits(models.Model):
    codeproduit = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produits'

class Contenir(models.Model):
    nofacture = models.OneToOneField('Factures', models.DO_NOTHING, db_column='nofacture', primary_key=True)
    codeproduit = models.ForeignKey('Produits', models.DO_NOTHING, db_column='codeproduit')

    class Meta:
        managed = False
        db_table = 'contenir'
        unique_together = (('nofacture', 'codeproduit'),)

class Paramgraph(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    nomgraph = models.CharField(max_length=50)
    param1 = models.IntegerField()
    param2 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'paramgraph'