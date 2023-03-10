# Generated by Django 4.1.6 on 2023-02-08 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('login', models.CharField(max_length=40, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(blank=True, max_length=40, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=40, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=40, unique=True, verbose_name='email')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True, verbose_name='Номер телефона')),
                ('date_birth', models.DateField(null=True, verbose_name='Дата рождения')),
                ('status', models.CharField(default='st', max_length=3, verbose_name='Тарифный план')),
                ('is_stuff', models.BooleanField(default=False)),
                ('is_activ', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользватель',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='User_instagram_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(blank=True, max_length=40, unique=True, verbose_name='Instagram пользователя')),
                ('password', models.CharField(blank=True, max_length=40, verbose_name='Пароль пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Instagram акаунт пользователя',
                'verbose_name_plural': 'Instagram акаунты пользователя',
            },
        ),
    ]
