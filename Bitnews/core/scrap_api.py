import json
import re
import codecs
import logging
import datetime
import io
import sys
import urllib2
import pytz
from bs4 import BeautifulSoup, BeautifulStoneSoup

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core import serializers
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.db.models.query_utils import Q
from django.db.transaction import atomic

from base_api import CustomBaseModelResource
from utils import generate_unique_customer_id
from .models import UserProfile, Category, Language
from news.models import News, NewsCategory, NewsLanguage
from feeds.models import NewsFeedItems, Feeds


logger = logging.getLogger("bitnews")

#################### Django REST FRAMEWORK API#####################

def keydata(item):
    for key in item:
        try:
            if key=='link':
                d1 = str(item[key])
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2[1:]

            if key=='description':
                d3 = str(item[key])
                # for extracting image url from descrption
                temp = [d3]
                soup = BeautifulSoup(''.join(temp))
                link=soup.find('a')
                try:    
                    image_url=link.contents[0]['src']
                except:
                    image_url=None
                
                if image_url==None:
                    break
                elif image_url=='':
                    break
                
                d4 = d3.strip("[").strip("]").replace(",","").replace("'","").replace("\\","")
                temp_desc = d4[1:]
                news_description=re.sub('<[^>]+>', '', temp_desc)
            if key=='title':
                d5 = str(item[key])
                tempd5=d5.replace("\u2018", "'").replace("\u2019", "'")
                d6 = tempd5.strip("[").strip("]").replace("'","").replace("\u","").replace('"','')
                news_title = d6[1:]
            if key=='pubdate':
                d7 = str(item[key])
                d8 = d7.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d8[6:-4]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
             # news_pubdate = datetime.datetime.strftime(news_pubdate_format,'%a, %d %b %Y %H:%M:%S')
        except:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)

def keydata_news18(item):
    for key in item:
        try:
            if key=='link':
                d1 = str(item[key])
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2[1:]
            if key=='description':
                d3 = str(item[key])
                # for extracting image url from descrption
                temp = [d3]
                soup = BeautifulSoup(''.join(temp))
                link=soup.findAll('img')[0].get('src')
                try:    
                    image_url=link
                except:
                    image_url=None
                
                if image_url==None:
                    break
                elif image_url=='':
                    break
                tempd3=d3.replace("&quot;","")
                d4 = tempd3.strip("[").strip("]").replace(",","").replace("'","").replace("\\","")
                temp_desc = d4[1:]
                news_description=re.sub('<[^>]+>', '', temp_desc)
            if key=='title':
                d5 = str(item[key])
                tempd5=d5.replace("\u2018", "'").replace("\u2019", "'")
                d6 = tempd5.strip("[").strip("]").replace("'","").replace("\u","").replace('"','')
                news_title = d6[1:]
            if key=='pubdate':
                d7 = str(item[key])
                d8 = d7.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d8[6:-6]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
             # news_pubdate = datetime.datetime.strftime(news_pubdate_format,'%a, %d %b %Y %H:%M:%S')
        except Exception as e:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)

def keydata_thestar(item):
    for key in item:
        try:
            if key=='link':
                d1 = str(item[key])
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2[1:]
            
            if key=='description':
                d3 = str(item[key])
                d4 = d3.strip("[").strip("]").replace(",","").replace("'","").replace("\\","")
                temp_desc = d4[1:]
                news_description=temp_desc
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url=='':
                    break

            if key=='title':
                d5 = str(item[key])
                tempd5=d5.replace("\u2018", "'").replace("\u2019", "'")
                d6 = tempd5.strip("[").strip("]").replace("'","").replace("\u","").replace('"','').replace("&#39;","`")
                news_title = d6[1:]
            
            if key=='pubdate':
                d7 = str(item[key])
                d8 = d7.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d8[6:-7]
                news_pubdate1 = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
                new_time=news_pubdate1-datetime.timedelta(hours=8)
                news_pubdate=new_time

        except Exception as e:
            break
    
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)


def keydata_zeenews(item):
    for key in item:
        try:
            if key=='link':
                d1 = str(item[key])
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2[30:]
            
            if key=='description':
                d3 = str(item[key])
                tempd3 = d3.replace("\\xa0"," ").replace("\\n","").replace("&quot;"," ").replace("&#039;"," ").\
                        replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", " ")
                d4 = tempd3.strip("[").strip("]").replace(",","").replace("'","").replace("\\","")
                temp_desc = d4[2:]
                news_description=temp_desc
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url=='':
                    break

            if key=='title':
                d5 = str(item[key])
                tempd5=d5.replace("\u2018", "'").replace("\u2019", "'").replace("&amp;#039;","")
                d6 = tempd5.strip("[").strip("]").replace("'","").replace("\u","").replace('"','').replace("&#39;","`")
                news_title = d6[1:]
            
            if key=='pubdate':
                d7 = str(item[key])
                d8 = d7.strip("[").strip("]").replace("'","")
                try:
                    news_temp_pubdate = d8[1:-10]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%A, %B %d, %Y, %H:%M')
                except:
                    news_temp_pubdate = d8[1:-8]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%A, %B %d, %Y, %H:%M')

        except Exception as e:
            break
    
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)


def keydata_zeenews_bengali(item):
    for key in item:
        try:
            if key=='link':
                d1 = str(item[key])
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2[42:]
            
            if key=='description':
                d3 = item[key]
                for i in d3:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d4 = a.replace("&nbsp;"," ").replace("&amp;#039;","")
                news_description = d4
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url=='':
                    break

            if key=='title':
                d5 = item[key]
                for i in d5:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d6= a.replace("&nbsp;"," ").replace("&amp;#039;","")
                news_title = d6

            if key=='pubdate':
                d7 = str(item[key])
                d8 = d7.strip("[").strip("]").replace("'","")
                try:
                    news_temp_pubdate = d8[1:-10]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%m/%d/%Y %H:%M')
                except:
                    news_temp_pubdate = d8[1:-8]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%-m/%d/%Y %H:%M')

        except Exception as e:
            break
    
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)


def keydata_other(item):
    for key in item:
        try:    
            if key=='link':
                d1 = item[key]
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2

            if key=='description':
                d3 = item[key]
                # for extracting image url from descrption
                for i in d3:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d4 = a.replace("&nbsp;"," ") 
                news_description=d4
            
            if key=='title':
                d0=item[key]
                for i in d0:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d5 = a.replace("&nbsp;"," ")
                news_title = d5
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url=='':
                    break
            if key=='pubdate':
                d8 = str(item[key])
                d9 = d8.strip("[").strip("]")
                news_temp_pubdate = d9[7:-7]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
        except:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)

def keydata_other_dainik(item):
    for key in item:
        try:
            if key=='link':
                d1 = item[key]
                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2

            if key=='description':
                d3 = item[key]
                # for extracting image url from descrption
                for i in d3:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d4 = a.replace("&nbsp;"," ") 
                news_description=d4
            
            if key=='title':
                d0=item[key]
                for i in d0:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d5 = a.replace("&nbsp;"," ").replace("\\","")
                news_title = d5
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url is None:
                    break
            if key=='pubdate':
                d8 = str(item[key])
                d9 = d8.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d9[6:-4]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
        except:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)

def keydata_other_jagran(item):
    for key in item:
        try:
            if key=='link':
                d1 = item[key]
                d2 = d1[0].strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2

            if key=='description':
                d3 = item[key]

                temp = d3
                soup = BeautifulSoup(''.join(temp))
                link=soup.findAll('img')[0].get('src')
                try:    
                    image_url=link
                except:
                    image_url=None
                
                if image_url==None:
                    break
                elif image_url=='':
                    break

                for i in d3:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d4 = a.replace("&nbsp;"," ") 
                news_description=re.sub('<[^>]+>', '', d4)
            
            if key=='title':
                d0=item[key]
                for i in d0:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d5 = a.replace("&nbsp;"," ").replace("\\","")
                news_title = d5
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url is None:
                    break
            if key=='pubdate':
                d8 = str(item[key])
                d9 = d8.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d9[2:-4]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')
        except Exception as e:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)

def keydata_other_ibnlive(item):
    for key in item:
        try:
            if key=='link':
                d1 = item[key]

                d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                news_link = d2

            if key=='description':
                d3 = item[key]
                # for extracting image url from descrption
                for i in d3:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d4 = a.replace("&nbsp;"," ") 
                news_description=re.sub('<[^>]+>', '', d4)
            
            if key=='title':
                d0=item[key]
                for i in d0:
                    a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                d5 = a.replace("&nbsp;"," ").replace("\\","")
                news_title = re.sub('<[^>]+>', '', d5)
            
            if key=='image':
                d6=str(item[key])
                d7 = d6.strip("[").strip("]").replace("'","")
                image_url = d7[1:]
                if image_url is None:
                    break
            if key=='pubdate':
                d8 = str(item[key])
                d9 = d8.strip("[").strip("]").replace("'","")
                news_temp_pubdate = d9[1:-3]
                news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%A, %B %d, %Y %H:%M')
        except Exception as e:
            break
    proc_data={'news_link':news_link,'image_url':image_url,
        'news_description':news_description,'news_title':news_title,
        'news_pubdate':news_pubdate}
    return(proc_data)


#########################################################################################################
@api_view(['GET','POST'])
def read_file(request):
    filenames = [  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-business.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-cricket.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-edu.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-entertainment.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-health.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-india.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-lifestyle.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-sports.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-tech.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/toi-world.json',
                ]
################################### Dainik Bhaskar#####################################33
    # For opening in file is OS
    # with open('/home/some-user/Office/Bitnomix/bitnewsscrap/dainik.json', 'r') as f:
    #     json_string = f.read()
    #     f.close()

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/dainik-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_dainik(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Dainik Bhaskar', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/dainik-entertainment.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_dainik(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Dainik Bhaskar', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

##########################################JAGRAN HINDI###############################################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-world.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_dainik(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-entertainment.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-education.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Education')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/jagran-cricket.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_jagran(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Cricket')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Jagran', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

##########################################AMARUJALA HINDI#############################################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/amarujala-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='AmarUjala', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/amarujala-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='AmarUjala', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/amarujala-lifestyle.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Lifestyle')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='AmarUjala', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/amarujala-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='AmarUjala', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/amarujala-tech.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='AmarUjala', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

####################################ONE INDIA KANNADA####################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/oneindia-kannada.json').read()
    data = json.loads(json_string)
    for item in data:
        try:
            for key in item:
                if key=='link':
                    d1 = item[key]
                    d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                    news_link = d2

                if key=='description':
                    d3 = item[key]
                    # for extracting image url from descrption
                    for i in d3:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d4 = a.replace("&nbsp;"," ") 
                    news_description=d4
                
                if key=='title':
                    d0=item[key]
                    for i in d0:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d5 = a.replace("&nbsp;"," ")
                    news_title = d5
                
                if key=='image':
                    d6=str(item[key])
                    d7 = d6.strip("[").strip("]").replace("'","")
                    image_url = d7[1:]
                    if image_url=='':
                        break
                    elif image_url is None:
                        break
                if key=='pubdate':
                    d8 = str(item[key])
                    d9 = d8.strip("[").strip("]").replace("'","")
                    news_temp_pubdate = d9[6:-6]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')

                news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
                news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Kannada')

            s, created= News.objects.get_or_create(title=news_title, content=news_description,source='One India', 
                                link=news_link, pubdate=news_pubdate, image_url=image_url,
                                category=news_cat, language=news_lang)
        except:
            continue
# ######################################ONE INDIA TELUGU#####################

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/oneindia-telugu.json').read()
    data = json.loads(json_string)
    for item in data:
        try:
            for key in item:
                if key=='link':
                    d1 = item[key]
                    d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                    news_link = d2

                if key=='description':
                    d3 = item[key]
                    # for extracting image url from descrption
                    for i in d3:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d4 = a.replace("&nbsp;"," ") 
                    news_description=d4
                
                if key=='title':
                    d0=item[key]
                    for i in d0:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d5 = a.replace("&nbsp;"," ")
                    news_title = d5
                
                if key=='image':
                    d6=str(item[key])
                    d7 = d6.strip("[").strip("]").replace("'","")
                    image_url = d7[1:]
                    
                    if image_url=='':
                        break
                    elif image_url is None:
                        break
                
                if key=='pubdate':
                    d8 = str(item[key])
                    d9 = d8.strip("[").strip("]").replace("'","")
                    news_temp_pubdate = d9[6:-6]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')

                news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
                news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Telugu')

            s, created= News.objects.get_or_create(title=news_title, content=news_description,source='One India', 
                                link=news_link, pubdate=news_pubdate, image_url=image_url,
                                category=news_cat, language=news_lang)
        except:
            continue
# ######################################ONE INDIA TAMIL######################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/oneindia-tamil.json').read()
    data = json.loads(json_string)
    for item in data:
        try:
            for key in item:
                if key=='link':
                    d1 = item[key]
                    d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                    news_link = d2

                if key=='description':
                    d3 = item[key]
                    # for extracting image url from descrption
                    for i in d3:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d4 = a.replace("&nbsp;"," ") 
                    news_description=d4
                
                if key=='title':
                    d0=item[key]
                    for i in d0:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d5 = a.replace("&nbsp;"," ")
                    news_title = d5
                
                if key=='image':
                    d6=str(item[key])
                    d7 = d6.strip("[").strip("]").replace("'","")
                    image_url = d7[1:]
                    if image_url is None:
                        break
                if key=='pubdate':
                    d8 = str(item[key])
                    d9 = d8.strip("[").strip("]").replace("'","")
                    news_temp_pubdate = d9[6:-6]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%d %b %Y %H:%M:%S')

                news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
                news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Tamil')

            s, created= News.objects.get_or_create(title=news_title, content=news_description,source='One India', 
                                link=news_link, pubdate=news_pubdate, image_url=image_url,
                                category=news_cat, language=news_lang)
        except:
            continue
# #######################################LOK SATTA- MARATHI############################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/loksatta.json').read()
    data = json.loads(json_string)
    for item in data:
        try:
            for key in item:
                if key=='link':
                    d1 = item[key]
                    d2 = d1.strip("[").strip("]").replace("'","").replace(", u",",\n")
                    news_link = d2

                if key=='description':
                    d3 = item[key]
                    # for extracting image url from descrption
                    for i in d3[0]:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d4 = a.replace("&nbsp;"," ")
                    d4=d3[0].encode("utf-8",errors="ignore")
                    news_description=d4
                
                if key=='title':
                    d0=item[key]
                    for i in d0:
                        a= codecs.BOM_UTF8 + i.encode("utf-8",errors="ignore")
                    d5 = a.replace("&nbsp;"," ")
                    news_title = d5
                
                if key=='image':
                    d6=str(item[key])
                    d7 = d6.strip("[").strip("]").replace("'","")
                    image_url = d7[1:]
                    if not image_url:
                        break
                if key=='pubdate':
                    d8 = str(item[key])
                    d9 = d8.strip("[").strip("]").replace("T"," ")
                    news_temp_pubdate = d9[2:-7]
                    news_pubdate = datetime.datetime.strptime(news_temp_pubdate,'%Y-%m-%d %H:%M:%S')

                news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
                news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Marathi')

            s, created= News.objects.get_or_create(title=news_title, content=news_description,source='Loksatta', 
                                link=news_link, pubdate=news_pubdate, image_url=image_url,
                                category=news_cat, language=news_lang)
        except Exception as e:
            continue

#################################ZEENEWS BENGALI################################
    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-bengali-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews_bengali(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Bengali')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-bengali-world.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews_bengali(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Bengali')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-bengali-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews_bengali(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Bengali')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-bengali-entertainment.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews_bengali(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Bengali')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

########################################TIMES OF INDIA########################'Times of India'
    json_string = json_string = urllib2.urlopen(filenames[0]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India', 
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[1]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Cricket')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                            image_url=item['image_url'],link=item['news_link'], pubdate=item['news_pubdate'], 
                            category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[2]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Education')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)                  
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[3]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[4]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Health')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[5]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            
                
            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[6]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            
  
            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Lifestyle')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[7]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[8]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            try:
                item=keydata(items)
            except:
                continue
            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(filenames[9]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            
                
            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Times of India',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
# # ###########################################EconomicTimes Files
    et_filenames = [ 'https://bitnews2.s3.amazonaws.com/scrapedjson/et-economy.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-industry.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-jobs.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-magazines.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-markets.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-smallbiz.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-tech.json',
                  'https://bitnews2.s3.amazonaws.com/scrapedjson/et-wealth.json',
                ]

    json_string = json_string = urllib2.urlopen(et_filenames[0]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Economy')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[1]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Industry')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[2]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Jobs')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[3]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Magazines')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[4]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Markets')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[5]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Smallbiz')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[6]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen(et_filenames[7]).read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Wealth')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Economic Times',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
################################THE STAR ENGLISH##############################################
    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/thestar-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_thestar(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='The Star',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/thestar-world.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_thestar(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='The Star',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/thestar-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_thestar(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='The Star',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/thestar-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_thestar(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='The Star',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/thestar-education.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_thestar(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Education')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='The Star',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
##########################################NEWS18########################################

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-world.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-tech.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/news18-lifestyle.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_news18(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Lifestyle')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='News18',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
#############################################ZEE NEWS ENGLISH#################################################END OF NEWS18
    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-world.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='World')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-tech.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/zee-entertainment.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_zeenews(items)            

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='English')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='Zee News',
                                link=item['news_link'], pubdate=item['news_pubdate'],image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

######################################IBNLIVE HINDI########################################
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-india.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='India')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-business.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Business')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-sports.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Sports')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-tech.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Tech')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-entertainment.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Entertainment')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue
    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-cricket.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Cricket')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    json_string = urllib2.urlopen('https://bitnews2.s3.amazonaws.com/scrapedjson/ibnlive-lifestyle.json').read()
    data = json.loads(json_string)
    for items in data:
        try:
            item=keydata_other_ibnlive(items)

            news_cat, news_cat1 = NewsCategory.objects.get_or_create(name='Lifestyle')
            news_lang, news_lang1 = NewsLanguage.objects.get_or_create(name='Hindi')

            s, created= News.objects.get_or_create(title=item['news_title'], content=item['news_description'],source='IBN Live', 
                                link=item['news_link'], pubdate=item['news_pubdate'], image_url=item['image_url'],
                                category=news_cat, language=news_lang)
        except:
            continue

    return Response({'message':'News saved succesfully', 'status':200})
