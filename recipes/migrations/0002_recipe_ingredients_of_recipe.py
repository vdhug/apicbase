# Generated by Django 2.0 on 2019-02-27 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0007_auto_20190227_1729'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients_of_recipe',
            field=models.ManyToManyField(through='recipes.IngredientOfRecipe', to='ingredients.Ingredient'),
        ),
    ]
