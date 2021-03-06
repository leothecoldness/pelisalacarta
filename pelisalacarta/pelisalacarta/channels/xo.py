﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F,S"
__language__ = "RU"
__title__ = "XO (RO)"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 0
__adult__ = False
__date__ = ""
__creationdate__ = "23/12/2013"
__changes__ = ""
__thumbnail__ = ""
__channel__ = "xo"

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.xo mainlist")
    item.url="http://xo.ro/"; 
    return novedades(item)

def novedades(item):
    logger.info("pelisalacarta.channels.xo novedades")
    itemlist = []
	
    # Descarga la página
    data = scrapertools.cachePage(item.url)
	
    '''
    <div class="views-row">
    <div class="views-field-field-image-fid">
    <span class="field-content">
    <a href="/filme-online/Ask-Me-Anything-3376">
    <img src="http://xo.ro//uploads/Ask-Me-Anything-poster.jpg" width="137" height="160" alt="Ask Me Anything"/>            </a>
    '''
    patron = '<div class="views-row"[^<]+'
    patron += '<div class="views-field-field-image-fid"[^<]+'
    patron += '<span class="field-content"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)" width="\d+" height="\d+" alt="([^"]+)"/>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
	
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if (DEBUG): logger.info("url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], title=["+scrapedtitle+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=urlparse.urljoin(item.url,scrapedurl) , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    

    next_page = scrapertools.find_single_match(data,'<a href="([^"]+)">\&gt\;</a>')	
    if next_page!="":
       itemlist.append( Item(channel=__channel__, action="novedades", title=">> Página urmatoare" , url=urlparse.urljoin(item.url,next_page) , folder=True) )
    return itemlist
