# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por boludiko
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "ES"
__title__ = "xhamster"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 5
__adult__ = True
__date__ = "26/04/2015"
__creationdate__ = ""
__changes__ = "Corregido"
__thumbnail__ = ""
__channel__ = "xhamster"

import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[xhamster.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"      , title="Útimos videos" , url="http://es.xhamster.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"    , title="Listado Categorias", url="http://es.xhamster.com/channels.php"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://xhamster.com/search.php?q=%s&qcat=video"))
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[xhamster.py] search")
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % tecleado
    return videos(item)

# SECCION ENCARGADA DE BUSCAR

def videos(item):
    logger.info("[xhamster.py] videos")
    data = scrapertools.cache_page(item.url)
    try:
      data = scrapertools.get_match(data,'<div class=\'video new-date\'>(.*?)<div id="footer">')
    except:
      pass
    itemlist = []
    
    patron = "<a href='([^']+)'  class='hRotator' ><img src='([^']+)' class='thumb' alt=\"([^\"]+)\"/>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,title in matches:
        try:
            scrapedtitle = unicode( title, "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = title
        scrapedurl = urlparse.urljoin( "http://www.xhamster.com" , url )
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, folder=False))
        
    # EXTRAE EL PAGINADOR
    patronvideos  = "<a href='([^']+)' class='last colR'><div class='icon iconPagerNextHover'>"
    siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(siguiente)
    if len(siguiente)>0:
        itemlist.append( Item(channel=__channel__, action='videos' , title=">> Pagina siguiente" , url=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] ), thumbnail="", plot="", show="!Página siguiente") )
    else:
        paginador = None

    return itemlist
    
def listcategorias(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="hetero" , title="Heterosexual", url="http://es.xhamster.com/channels.php"))
    itemlist.append( Item(channel=__channel__, action="trans" , title="Transexuales", url="http://es.xhamster.com/channels.php"))
    itemlist.append( Item(channel=__channel__, action="gay" , title="Gays", url="http://es.xhamster.com/channels.php"))
    return itemlist

    
def hetero(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="title">Heterosexual</div>(.*?)<div class="title">Transexuales</div>')
    itemlist = []
    
    patron = '<a class="btnBig" href="([^"]+)">[ |\n]*(?:<div[^>]*></div>)?(?:<div[^>]*>[ |\n]*<img[^>]*>[ |\n]*</div>)?[ |\n]*(.*?)[ |\n]*</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches: 
      itemlist.append( Item(channel=__channel__, action="videos" , title=title.strip(), url=url))
    itemlist.sort(key=lambda item: item.title.lower().strip())
    return itemlist

def trans(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="title">Transexuales</div>(.*?)<div class="title">Gays</div>')
    itemlist = []
    
    patron = '<a class="btnBig" href="([^"]+)">[ |\n]*(?:<div[^>]*></div>)?(?:<div[^>]*>[ |\n]*<img[^>]*>[ |\n]*</div>)?[ |\n]*(.*?)[ |\n]*</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches: 
      itemlist.append( Item(channel=__channel__, action="videos" , title=title.strip(), url=url))
    itemlist.sort(key=lambda item: item.title.lower().strip())
    return itemlist

def gay(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="title">Gays</div>(.*?)<div id="footer">')
    itemlist = []
    
    patron = '<a class="btnBig" href="([^"]+)">[ |\n]*(?:<div[^>]*></div>)?(?:<div[^>]*>[ |\n]*<img[^>]*>[ |\n]*</div>)?[ |\n]*(.*?)[ |\n]*</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches: 
      itemlist.append( Item(channel=__channel__, action="videos" , title=title.strip(), url=url))
    itemlist.sort(key=lambda item: item.title.lower().strip())
    return itemlist   

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def play(item):
    logger.info("[xhamster.py] play")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    #logger.debug(data)

    url = scrapertools.get_match(data,'<video poster="[^"]+" type=\'video/mp4\' file="([^"]+)"')
    logger.debug("url="+url)
    itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="directo", folder=False))
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_itemlist = mainlist(Item())
    video_itemlist = videos(mainlist_itemlist[0])
    
    # Si algún video es reproducible, el canal funciona
    for video_item in video_itemlist:
        play_itemlist = play(video_item)

        if len(play_itemlist)>0:
            return True

    return False