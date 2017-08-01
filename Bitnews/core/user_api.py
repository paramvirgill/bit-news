import json
import re
import logging
import datetime
from operator import itemgetter
from bs4 import BeautifulSoup, BeautifulStoneSoup

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash
from tastypie.resources import Resource, ModelResource
from tastypie.utils.mime import determine_format
from tastypie.http import HttpBadRequest
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.fields import ApiField
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.paginator import Paginator

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination

from django.core import serializers
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.db.models.query_utils import Q

from base_api import CustomBaseModelResource
from utils import generate_unique_customer_id
from .models import UserProfile, Category, Language
from news.models import News, NewsCategory, NewsLanguage
from feeds.models import NewsFeedItems, Feeds


logger = logging.getLogger("bitnews")

class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        output['page_number'] = int(self.offset / self.limit) + 1
        return output

class DjangoUserResources(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization
        allowed_methods = ['get', 'post', 'put']
        excludes = ['password', 'is_superuser']
        always_return_data = True

class BitUserResource(CustomBaseModelResource):

    user = fields.ForeignKey(DjangoUserResources, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = "bitusers"
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "consumer_id": ALL
                     }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('user_registration'), name="user_registration"),
            url(r"^(?P<resource_name>%s)/preference-save%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('user_preference'), name="user_preference"),

			]


    def create_user(self, is_active, device_id, email=None):
        consumer_id = generate_unique_customer_id()
        password = consumer_id+settings.PASSWORD_POSTFIX
        user_obj = User.objects.create(username=consumer_id)
        user_obj.set_password(password)
        user_obj.is_active = is_active
        if email:
            user_obj.email=email
        user_obj.save()
        bituser_obj = UserProfile(user=user_obj,device_id=device_id)
                                                              
        bituser_obj.save()
        return {'bituser_obj': bituser_obj}
 
    def user_registration(self, request, **kwargs):
        '''
        Register user with valid device id
        Args : device id
        '''
        device = request.GET['device_id']
        if not device:
            return HttpBadRequest("Enter device id")
        try:
            device_id=str(device)
            bituser = UserProfile.objects.get(device_id=device_id)

            if bituser:
                data = {}
               
                for i in allinterest_data:
                    i['accepted']=0

                alllanguage_data =[model_to_dict(c, exclude='image_url') for c in Language.objects.all().order_by('id')]
                for i in alllanguage_data:
                    i['accepted']=0

                interest_data=[model_to_dict(c, exclude='image_url') for c in bituser.interests_category.all().order_by('id')]
                for i in interest_data:
                    i['accepted']=1

                language_data = [model_to_dict(c, exclude='image_url') for c in bituser.user_languages.all().order_by('id')]
                for i in language_data:
                    i['accepted']=1
                interest_list=[]
                for i in allinterest_data + interest_data:
                    interest_list.append(i)
                final_interest={v['name']:v for v in interest_list}.values()  
                final_interest1 = sorted(final_interest, key=itemgetter('id')) 
                data['interests']=final_interest1

                language_list=[]
                for i in alllanguage_data + language_data:
                    language_list.append(i)
                final_language={v['name']:v for v in language_list}.values()
                final_language1 = sorted(final_language, key=itemgetter('id')) 
                data['languages']=final_language1

                #For fetching Category Image_url with ID
                cat_obj=Category.objects.all().order_by('id')
                cat_list=[]
                for i in cat_obj:
                    d={}
                    d['id']=i.id
                    d['image_url']=i.image_url.name
                    cat_list.append(d)
                data['category_images']=cat_list

                #For fetching Languages Image_url with ID
                lang_obj=Language.objects.all().order_by('id')
                lang_list=[]
                for i in lang_obj:
                    d={}
                    d['id']=i.id
                    d['image_url']=i.image_url.name
                    lang_list.append(d)
                data['language_images']=lang_list

                data = {'status_code':200,'bituser_details': data}
                return HttpResponse(json.dumps(data), content_type="application/json")

        except Exception as ObjectDoesNotExist:
            logger.info('Exception while fetching user - {0}'.format(device_id))
            try:
                user_obj = self.create_user(True, device_id=device_id)
                bituser_obj = user_obj['bituser_obj']
                
                data = {}
                allinterest_data =[model_to_dict(c ,exclude='image_url') for c in Category.objects.all().order_by('id')]
                for i in allinterest_data:
                    i['accepted']=0

                alllanguage_data =[model_to_dict(c, exclude='image_url') for c in Language.objects.all().order_by('id')]
                for i in alllanguage_data:
                    i['accepted']=0

                data['interests']= allinterest_data
                data['languages']=alllanguage_data

                cat_obj=Category.objects.all().order_by('id')
                cat_list=[]
                for i in cat_obj:
                    d={}
                    d['id']=i.id
                    d['image_url']=i.image_url.name
                    cat_list.append(d)
                data['category_images']=cat_list

                #For fetching Languages Image_url with ID
                lang_obj=Language.objects.all().order_by('id')
                lang_list=[]
                for i in lang_obj:
                    d={}
                    d['id']=i.id
                    d['image_url']=i.image_url.name
                    lang_list.append(d)
                data['language_images']=lang_list

                data = {'status':1, 'message': 'Device registered successfully','bituser_details': data}
                return HttpResponse(json.dumps(data), content_type="application/json")
            
            except Exception as ex:
                    logger.info("Exception while registering user with device id - {0}".format(ex))
                    return HttpBadRequest("Device could not be registered")


    def user_preference(self, request, **kwargs):
        '''
        Register user with valid device id
        Args : device id
        '''
        load = json.loads(request.body)
        interests = load.get('interests')
        languages = load.get('languages')
        device_id = load.get('device_id')
        
        try:
            user_obj=UserProfile.objects.get(device_id=device_id)
        except:
                return HttpBadRequest("Enter valid device id")
        try:
            cat_list=[]
            lang_list=[]
            #For appending keys in a list
            for i in interests:
                for j,k in i.items():
                    cat_list.append(k)
            for i in languages:
                for j,k in i.items():
                    lang_list.append(k)
            #For saving list of key item in models
            #Saving in Categories
            if cat_list:
                user_obj.interests_category.clear()
            for i in cat_list:
                try:
                    cat_obj=Category.objects.get(name=i)
                    user_obj.interests_category.add(cat_obj)
                except: 
                    pass
            #Saving in Languages
            if lang_list:
                user_obj.user_languages.clear()
            for i in lang_list:
                try:
                    lang_obj=Language.objects.get(name=i)
                    user_obj.user_languages.add(lang_obj)
                except: 
                    pass
            data = {'status':1, 'message': 'Updated successfully'}
            return HttpResponse(json.dumps(data), content_type="application/json")
        
        except Exception as ex:
                logger.info("Exception while updating user details with device id - {0}".format(ex))
                return HttpBadRequest("Update failed")

#################### Django REST FRAMEWORK API#####################
########################################TO BE MOVED TO SCRAP API
@api_view(['GET','POST'])
def news_to_feeds(request):
    try:
        news_objs=News.objects.all()
        for news_obj in news_objs:
           s, created = NewsFeedItems.objects.get_or_create(language=news_obj.language,
                                        category=news_obj.category,
                                        image_url=news_obj.image_url,
                                        content=news_obj.content,
                                        pubdate=news_obj.pubdate,
                                        source=news_obj.source,
                                        title=news_obj.title,
                                        link=news_obj.link)
        return Response({'message':'News saved to Feeds succesfully', 'status':200})
    
    except Exception as ex:
            logger.info("Exception while updating user details with device id - {0}".format(ex))

    return HttpBadRequest("Update failed")


@api_view(['GET'])
def feeds_to_user(request):
    device = request.GET['device_id']
    if not device:
        return HttpBadRequest("Enter device id")

    user_obj=UserProfile.objects.get(device_id = device)
    user_interests = user_obj.interests_category.all()
    user_languages = user_obj.user_languages.all()
    paginator = PageNumberPagination()

    interest_list=[]
    language_list=[]
    for interest in user_interests:
        interest_list.append(interest)
    for language in user_languages:
        language_list.append(language)

    newsfeeds_objs1 = NewsFeedItems.objects.filter(category__in=interest_list)\
                                            .filter(language__in=language_list)\
                                            .order_by('-pubdate')
    if not newsfeeds_objs1:

        newsfeeds_objs1 = NewsFeedItems.objects.filter(language__in=language_list)\
                                                            .order_by('-pubdate')

    newsfeeds_objs = paginator.paginate_queryset(newsfeeds_objs1, request)

    feed_item=[]
    for newsfeeds_obj in newsfeeds_objs:
        user_feeds={}
        user_feeds['title']=newsfeeds_obj.title
        user_feeds['descrption']=newsfeeds_obj.content
        user_feeds['image_url']=newsfeeds_obj.image_url
        news_pubdate = datetime.datetime.strftime(newsfeeds_obj.pubdate,'%a, %d %b %Y %H:%M')
        user_feeds['pubdate']=str(news_pubdate)
        user_feeds['link']=newsfeeds_obj.link
        user_feeds['category']=newsfeeds_obj.category
        user_feeds['language']=newsfeeds_obj.language
        user_feeds['source']=newsfeeds_obj.source
        feed_item.append(user_feeds)

    data = {'status_code':200,'feeds_details': feed_item}
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET' ,'POST'])
def interest_update(request):
    newscat_obj=NewsCategory.objects.all()
    for obj in newscat_obj:
        try:
            usercat_obj= Category.objects.get(name=obj.name)
        except:
            cat_list=[]
            user={}
            user['list']=obj.name
            cat_list.append(user)
            usercat_obj=Category(name=obj.name)
            usercat_obj.save()

    data = {'status_code':200,'cat_list': cat_list}

    return Response(data, status=status.HTTP_201_CREATED)
