# Generated by Django 3.2.4 on 2021-07-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210701_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(choices=[('Mrs', 'Mrs'), ('Mr', 'Mr'), ('Dr(Mrs)', 'Dr Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Prof(Mrs)', 'Prof Mrs')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='staff_id',
            field=models.CharField(blank=True, default='AM-2021-7-NBGIIODYZ', max_length=6, null=True),
        ),
    ]