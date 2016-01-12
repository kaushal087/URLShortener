from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import turl

from  BeautifulSoup import BeautifulSoup
import requests
import urllib2

from django.http import JsonResponse
from django.core import serializers
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.conf import settings

import socket



import os.path
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


def getNoOfHits(request):
	shorturl = str(request.GET["url"])
	urlid = int(getURLId(shorturl))

	try:
		urlObj = turl.objects.get(urlid=urlid)
	except:
		raise Http404("Page not found")

	#current_site = socket.gethostbyname(socket.gethostname())
	#current_site = socket.gethostbyaddr()
	current_site = settings.SITE_URL

	d = {}
	d["shorturl"] =  current_site + "/url/" +  str(urlObj.surl)
	d["hits"] = urlObj.hits

	return JsonResponse(d, safe=False)	



def searchURL(request):

	searchString = request.GET["searchString"]
	#searchString = "Goo"

	urlObj = turl.objects.only('url', 'surl', 'title')

	lst = []

	for urlrow in urlObj:
		current_title = urlrow.title
		print current_title
		if(current_title.lower().find(searchString.lower()) > -1):
			d = {}
			d["url"] = urlrow.url
			d["title"] = current_title
			lst.append(d)

	return JsonResponse(lst, safe=False)


def redirectToLongURL(request, shorturl):

	urlid = getURLId(shorturl)
	print "urlid", urlid

	urlid = int(urlid)
	try:
		urlObj = turl.objects.get(urlid=urlid)
	except:
		raise Http404("Page not found")
	print urlObj

	urlObj.hits += 1
	urlObj.save()
	url = str(urlObj.url)
	print "url", url
	return HttpResponseRedirect(url)


def index(request):
	# urllist =  turl.objects.all()
	# context = {'urllist': urllist}
	# for urlrow in urllist:
	# 	print urlrow.url
	# #print urllist
	full_url = request.build_absolute_uri(None)
	print full_url

	context = {}
	#context["current_site"] = socket.gethostbyname(socket.gethostname())
	context["current_site"] = full_url

	return render(request, 'shortner/index.html', context)


def showURLPage(request):
	full_url = request.build_absolute_uri(None)
	print full_url

	return render(request, 'shortner/surl.html', {})


def getShortURL(urlid):

	Map = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	shorturl = ""

	while(urlid != 0):
		shorturl  = shorturl + Map[urlid%62]
		urlid = urlid/62

	shorturl = shorturl[::-1]
	print "shorturl" ,  shorturl

	return shorturl

def getURLId(shorturl):

	urlid = 0

	for i in range(len(shorturl)):
		if('a' <= shorturl[i] and ord(shorturl[i]) <= ord('z') ):
			urlid = urlid*62 + ord(shorturl[i]) - ord('a')
		if('A' <= shorturl[i] and ord(shorturl[i]) <= ord('Z') ):
			urlid = urlid*62 + ord(shorturl[i]) - ord('A') + 26
		if('0' <= shorturl[i] and ord(shorturl[i]) <= ord('9') ):
			urlid = urlid*62 + ord(shorturl[i]) - ord('0') + 52

	return urlid


def shortenURL(request):
	url =  str(request.POST['longURL'])
	url = url.strip()
	url = str(url)
	context = {}

	urlPage = BeautifulSoup(urllib2.urlopen(url))
	if(urlPage.title == None):
		title = 'No title'
	else:
		title = urlPage.title.string

	title = str(title)
	print url
	print title

	objNewURL, isCreated = turl.objects.get_or_create(url = url, title=title)
	objNewURL.save()
	urlid = objNewURL.urlid
	shorturl = getShortURL(urlid)
	print shorturl
	objNewURL.surl = shorturl
	objNewURL.save()

	print shorturl

	#current_site = socket.gethostbyname(socket.gethostname())
	current_site = settings.SITE_URL

	shorturl =  current_site + "/url/" +  shorturl


	data = {"shorturl":shorturl}

	return JsonResponse(data, safe=False)
