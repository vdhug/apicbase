# Generated by Django 2.0 on 2019-02-27 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0005_auto_20190227_0237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['-last_modified', '-date_created']},
        ),
    ]
