# Generated by Django 5.0.1 on 2025-05-31 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='BanaRandevu', max_length=100, verbose_name='Site Adı')),
                ('welcome_message', models.TextField(blank=True, verbose_name='Karşılama Mesajı')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='İletişim Telefonu')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='İletişim E-posta')),
                ('facebook_url', models.URLField(blank=True, verbose_name='Facebook URL')),
                ('instagram_url', models.URLField(blank=True, verbose_name='Instagram URL')),
                ('twitter_url', models.URLField(blank=True, verbose_name='Twitter URL')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site/', verbose_name='Logo')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='site/', verbose_name='Favicon')),
                ('telegram_bot_enabled', models.BooleanField(default=False, verbose_name='Telegram Bot Aktif')),
                ('meta_title', models.CharField(blank=True, max_length=100, verbose_name='Meta Başlık')),
                ('meta_description', models.TextField(blank=True, verbose_name='Meta Açıklama')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, verbose_name='Meta Anahtar Kelimeler')),
            ],
            options={
                'verbose_name': 'Site Ayarları',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),
    ]
