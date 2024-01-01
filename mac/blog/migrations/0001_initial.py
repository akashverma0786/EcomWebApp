# Generated by Django 4.1.7 on 2023-05-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('head0', models.CharField(max_length=500)),
                ('chead0', models.TextField(max_length=50000)),
                ('head1', models.CharField(max_length=500)),
                ('chead1', models.TextField(max_length=50000)),
                ('head2', models.CharField(max_length=50)),
                ('chead2', models.TextField(max_length=50000)),
                ('pub_date', models.DateField()),
                ('thumbnail', models.ImageField(default='', upload_to='shop/images')),
            ],
        ),
    ]
