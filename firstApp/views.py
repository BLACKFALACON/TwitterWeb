from django.shortcuts import render, redirect,get_object_or_404
import requests
from .models import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from firstApp.forms import EmpForm
import tweepy 
import pandas as pd
import csv
from sklearn import model_selection, preprocessing, linear_model, metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition, ensemble
import pandas, numpy, textblob, string
from warnings import filterwarnings
filterwarnings('ignore')
from textblob import Word
import nltk
from nltk.corpus import stopwords


@login_required(login_url='/login/')
def IndexView(request):
    template_name='index.html'
    return render(request,template_name)

@login_required(login_url='/login/')
def HesapView(request):
    template_name='hesap.html'
    return render(request,template_name)

@login_required(login_url='/login/')
def ContactView(request):
    template_name='contact.html'
    contact = Contact.objects.filter(alıcı=request.user)
    cntfrm = EmpForm(request.POST or None)  
    if cntfrm.is_valid():
        message = cntfrm.save(commit=False)
        message.user = request.user
        message.save()
        return redirect('contact')
    return render(request,template_name,{'contact':contact,'form':cntfrm})


def ClearContact(requst,id):
    secilen=get_object_or_404(Contact,id=id)
    secilen.delete()
    return redirect('contact')


@login_required(login_url='/login/')
def AnalizView(request):  
    if not request.user.is_authenticated:
       return redirect('index')
    post = Post.objects.filter(user=request.user )
    dosya=request.GET.get('durum',default = 'None')
    print(dosya)
    if dosya == 'None':
        dosya=str(329)
    kf= pd.read_csv('media/'+dosya+'.csv', encoding='utf_8')  
    ld = pd.read_csv('media/'+dosya+'_LD.csv', encoding='utf_8')
    tk= pd.read_csv('media/'+dosya+'_TK.csv', encoding='utf_8')
    gd= pd.read_csv('media/'+dosya+'_GD.csv', encoding='utf_8')
    contex={
        'post':post,
        'kelimefrekans': kf.to_dict('records'),      
        'gundagilimi': gd.to_dict('records'),
        'tweetkaynak': tk.to_dict('records'),
        'lokasyondagilimi': ld.to_dict('records'),
    }
    return render(request,'analiz.html',contex)
    

# --------------

@login_required(login_url='/login/')
def AnalizEtView(request):
    template_name='otomatikanaliz.html'
    tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
    tweet = Tweets.objects.filter(user=request.user) 
    contex={
        'tweet':tweet,
        'tweet_all':tweet_all
    } 
    return render(request,template_name,contex)

def FilterTweet(request,hastag):
    template_name='otomatikanaliz.html'
    tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
    tweet = Tweets.objects.filter(hastag=hastag)
    return render(request,template_name,{'tweet':tweet,'tweet_all':tweet_all})

def AnalizGöster(request):
    template_name='otomatikanaliz.html'
    hastag=request.GET.get('hastag',default = 'None')
    adet=request.GET.get('tweetadet',default = 'None')
    user=request.user
    print(adet)
    print(hastag)
    if hastag != 'None' or adet != 'None':
        TweetAnalizi(hastag,adet,user)
        tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
        tweet = Tweets.objects.filter(user=request.user) 
        contex={
            'tweet':tweet,'tweet_all':tweet_all
        } 
        return render(request,template_name,contex)
    else:
        tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
        tweet = Tweets.objects.filter(user=request.user) 
        contex={
            'tweet':tweet,'tweet_all':tweet_all
        } 
        return render(request,template_name,contex)

def Tweetlers(hastag,adet):
    consumer_key ='SPi1R25BOz2HIZmQdpDAu8l3x'
    consumer_secret ='IeQ2X0wyV5uDWsxcHyx2hvkTY9hcXMYBDPyr4alevLszzZE6fZ'
    access_token ='1019708295043534850-ZNzdZQxFJFXvrrhiiRfFAihXv8rDRz'
    access_token_secret ='kmYYP876OjA9MoBGO8J04oY4iXuNc38lutFAU0OKGy8dn'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api=tweepy.API(auth)
    
    adet=int(adet)
    tweetler = api.search(q = hastag, lang = "tr", result_type = "recent", count =adet)
    id_list = [tweet.id for tweet  in tweetler]
    df = pd.DataFrame(id_list, columns = ["id"])
    df['text'] = [tweet.text for tweet in tweetler]
    df['screen_name'] = [tweet.author.screen_name  for tweet in tweetler]
    df['profile_image_url'] = [tweet.author.profile_image_url for tweet in tweetler]

    return df

def TweetAnalizi(hastag,adet,user):
    
    df=Tweetlers(hastag,adet)

    df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    df['text'] = df['text'].str.replace('[^\w\s]','')       
    df['text'] = df['text'].str.replace('http','') 
    df['text'] = df['text'].str.replace('\d','')
    sw = stopwords.words('turkish')
    df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
    df['text'] = df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 
    df['text'] = df['text'].str.replace('rt','') 
    df["sentiment"]=2
    df.to_csv('media/gelen.csv', mode='w',index=False)
    df = pd.read_csv('media/yorumlar.csv')

    train_x, test_x, train_y, test_y = model_selection.train_test_split(df["yorum"],df["Positivity"])
    encoder = preprocessing.LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    test_y = encoder.fit_transform(test_y)

    tf_idf_word_vectorizer = TfidfVectorizer()
    tf_idf_word_vectorizer.fit(train_x)
    x_train_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
    x_test_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)

    loj = linear_model.LogisticRegression()
    loj_model = loj.fit(x_train_tf_idf_word,train_y)

    df=pd.read_csv('media/gelen.csv', encoding='utf_8')
    for x in range(df['text'].count()):
        veri= pd.Series(df['text'][x])
        veri = tf_idf_word_vectorizer.transform(veri)
        sonuc=loj_model.predict(veri)
        sonuc=int(sonuc)
        if sonuc == 1 :
            df['sentiment'][x]=sonuc
        else:
            df['sentiment'][x]=sonuc

    df["sentiment"].replace(0, value = "Negatif", inplace = True)
    df["sentiment"].replace(1, value = "Pozitif", inplace = True)

    for i in range(len(df['text'])):
                tweet=Tweets()
                tweet.tweet=df.loc[i]['text']
                tweet.user=user
                tweet.hastag=hastag
                tweet.userName=df.loc[i]['screen_name']
                tweet.durum=df.loc[i]['sentiment']
                tweet.userAvatar=df.loc[i]['profile_image_url']
                tweet.save()
