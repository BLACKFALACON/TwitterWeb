from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey("auth.User", verbose_name=("Kullancı"), on_delete=models.CASCADE)
    dosyaNumarası=models.CharField(verbose_name='Dosya Numarası', max_length=100,primary_key=True)
    projeadi=models.CharField(verbose_name='Proje Adı', max_length=100)
    hastag=models.CharField(verbose_name='Hastag', max_length=100)
    tweetharitasi = models.ImageField(verbose_name='Kelime Haritası Resim',blank=True,null=True)

    tweetfrekans = models.ImageField(verbose_name='Kelime Frekans Resim',blank=True,null=True)
    tweetfrekanscsv = models.FileField(verbose_name='Kelime Frekans Csv Dosyası',blank=True,null=True)

    tweetkaynak = models.ImageField(verbose_name='Tweetlerin Atıldığı Kaynak Resim',blank=True,null=True)
    tweetkaynakcsv = models.FileField(verbose_name='Tweetlerin Atıldığı Kaynak Csv Kaynak',blank=True,null=True)

    tweetlokasyondagilim = models.ImageField(verbose_name='Tweet Lokasyon Dağılımı Resim', blank=True,null=True)
    tweetlokasyondagilimcsv = models.FileField(verbose_name='Tweet Lokasyon Dağılımı Csv Dosyası', blank=True,null=True)

    tweetgundagilimi = models.ImageField(verbose_name='Tweet Gün Dağılımı Resim',blank=True,null=True)
    tweetgundagilimicsv = models.FileField(verbose_name='Tweet Gün Dağılımı Csv Dosyası ',blank=True,null=True)

    tweetdosyasi = models.FileField(verbose_name='Tweet CSV Dosya Seçiniz',blank=True,null=True)
    retweet = models.FileField(verbose_name='Retweet CSV Dosya Seçiniz',blank=True,null=True)
    tweetozgunluk=models.CharField(verbose_name='Tweet Özgünlük Oranı', max_length=100,null=True)
    tweetsayisi = models.IntegerField(verbose_name='Toplam Tweet Sayısı',default=0)
    pozitifTweet = models.IntegerField(verbose_name='Pozitif Tweet Sayısı',default=0)
    negatifTweet = models.IntegerField(verbose_name='Negatif Tweet Sayısı',default=0)
    time=models.DateTimeField(verbose_name='Tarih',auto_now_add=True)
    class Meta:
        ordering = ['-time']

class Tweets(models.Model):
    user = models.ForeignKey("auth.User", verbose_name=("Kullancı "), on_delete=models.CASCADE)
    userName=models.CharField(verbose_name='Kullanıcı Adı ', max_length=100,blank=True,null=True)
    hastag=models.CharField(verbose_name='Hastag', max_length=100,blank=True,null=True)
    tweet=models.CharField(verbose_name='Tweet', max_length=200,blank=True,null=True)
    userAvatar = models.CharField(verbose_name='Avatar', max_length=500,blank=True,null=True)
    durum=models.CharField(verbose_name='Tweet', max_length=10,blank=True,null=True)
    time=models.DateTimeField(verbose_name='Tarih',auto_now_add=True,blank=True,null=True)
    class Meta:
        ordering = ['-time']

class Contact(models.Model):
    user = models.ForeignKey("auth.User",related_name="contacts", verbose_name=("Kullancı"), on_delete=models.CASCADE)
    alıcı = models.ForeignKey("auth.User",default=1,verbose_name=("Mesaj Gönderilen"), on_delete=models.CASCADE)
    konu=models.CharField(verbose_name='Konu', max_length=100)
    mesaj=models.TextField(verbose_name='Mesaj', max_length=600)
    time=models.DateTimeField(verbose_name='Tarih',auto_now_add=True)
    class Meta:
        ordering = ['-time']

