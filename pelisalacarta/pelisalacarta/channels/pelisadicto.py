# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "ES"
__title__ = "Pelisadicto"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 4
__adult__ = False
__date__ = "18/02/2015"
__creationdate__ = ""
__changes__ = "Eliminado del patr�n calidad de las fichas."
__thumbnail__ = ""
__channel__ = "pelisadicto"

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
    logger.info("[pelisadicto.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Últimas agregadas"  , action="agregadas", url="http://pelisadicto.com"))
    itemlist.append( Item(channel=__channel__, title="Listado por género" , action="porGenero", url="http://pelisadicto.com"))
    itemlist.append( Item(channel=__channel__, title="Buscar" , action="search", url="http://pelisadicto.com") )
    
    return itemlist

def porGenero(item):
    logger.info("[pelisadicto.py] porGenero")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Acción",url="http://pelisadicto.com/genero/Acción/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Adulto",url="http://pelisadicto.com/genero/Adulto/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Animación",url="http://pelisadicto.com/genero/Animación/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Aventura",url="http://pelisadicto.com/genero/Aventura/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Biográfico",url="http://pelisadicto.com/genero/Biográfico/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Ciencia Ficción",url="http://pelisadicto.com/genero/Ciencia Ficción/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Cine Negro",url="http://pelisadicto.com/genero/Cine Negro/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Comedia",url="http://pelisadicto.com/genero/Comedia/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Corto",url="http://pelisadicto.com/genero/Corto/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Crimen",url="http://pelisadicto.com/genero/Crimen/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Deporte",url="http://pelisadicto.com/genero/Deporte/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Documental",url="http://pelisadicto.com/genero/Documental/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Drama",url="http://pelisadicto.com/genero/Drama/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Familiar",url="http://pelisadicto.com/genero/Familiar/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Fantasía",url="http://pelisadicto.com/genero/Fantasía/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Guerra",url="http://pelisadicto.com/genero/Guerra/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Historia",url="http://pelisadicto.com/genero/Historia/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Misterio",url="http://pelisadicto.com/genero/Misterio/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Música",url="http://pelisadicto.com/genero/Música/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Musical",url="http://pelisadicto.com/genero/Musical/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Romance",url="http://pelisadicto.com/genero/Romance/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Terror",url="http://pelisadicto.com/genero/Terror/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Thriller",url="http://pelisadicto.com/genero/Thriller/1"))
    itemlist.append( Item(channel=__channel__ , action="agregadas" , title="Western",url="http://pelisadicto.com/genero/Western/1"))

    return itemlist	

def search(item,texto):
    logger.info("[pelisadicto.py] search")

    '''
    texto_get = texto.replace(" ","%20")
    texto_post = texto.replace(" ","+")
    item.url = "http://pelisadicto.com/buscar/%s?search=%s" % (texto_get,texto_post)
    '''

    texto_post = texto.replace(" ","+")
    item.url = "http://pelisadicto.com/buscar/%s" % texto

    try:
        return agregadas(item)
    # Se captura la excepci?n, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

    return busqueda(item)

def agregadas(item):
    logger.info("[pelisadicto.py] agregadas")
    itemlist = []
    '''
    # Descarga la pagina
    if "?search=" in item.url:
        url_search = item.url.split("?search=")
        data = scrapertools.cache_page(url_search[0], url_search[1])
    else:
        data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    '''

    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    # Extrae las entradas
    fichas = re.sub(r"\n|\s{2}","",scrapertools.get_match(data,'<ul class="thumbnails">(.*?)</ul>'))

    #<li class="col-xs-6 col-sm-2 CALDVD"><a href="/pelicula/101-dalmatas" title="Ver 101 dÃ¡lmatas Online" class="thumbnail thumbnail-artist-grid"><img class="poster" style="width: 180px; height: 210px;" src="/img/peliculas/101-dalmatas.jpg" alt="101 dÃ¡lmatas"/><div class="calidad">DVD</div><div class="idiomas"><img src="/img/1.png"  height="20" width="30" /></div><div class="thumbnail-artist-grid-name-container-1"><div class="thumbnail-artist-grid-name-container-2"><span class="thumbnail-artist-grid-name">101 dÃ¡lmatas</span></div></div></a></li>

    patron = 'href="([^"]+)".*?' # url
    patron+= 'src="([^"]+)" '    # thumbnail
    patron+= 'alt="([^"]+)'      # title

    matches = re.compile(patron,re.DOTALL).findall(fichas)
    for url,thumbnail,title in matches:
        url=urlparse.urljoin(item.url,url)
        thumbnail = urlparse.urljoin(url,thumbnail)

        itemlist.append( Item(channel=__channel__, action="findvideos", title=title+" ", fulltitle=title , url=url , thumbnail=thumbnail , show=title, viewmode="movie_with_plot") )

    # Paginación
    try:
    
        #<ul class="pagination"><li class="active"><span>1</span></li><li><span><a href="2">2</a></span></li><li><span><a href="3">3</a></span></li><li><span><a href="4">4</a></span></li><li><span><a href="5">5</a></span></li><li><span><a href="6">6</a></span></li></ul>

        current_page_number = int(scrapertools.get_match(item.url,'/(\d+)$'))
        item.url = re.sub(r"\d+$","%s",item.url)
        next_page_number = current_page_number + 1
        next_page = item.url % (next_page_number)
        itemlist.append( Item(channel=__channel__, action="agregadas", title="Página siguiente >>" , url=next_page) )
    except: pass

    return itemlist

def findvideos(item):
    logger.info("[pelisadicto.py] findvideos")

    itemlist = []

    data = re.sub(r"\n|\s{2}","",scrapertools.cache_page(item.url))

    #<!-- SINOPSIS --> <h2>Sinopsis de 101 dÃ¡lmatas</h2> <p>Pongo y Perdita, los dÃ¡lmatas protagonistas, son una feliz pareja canina que vive rodeada de sus cachorros y con sus amos Roger y Anita. Pero su felicidad estÃ¡ amenazada. Cruella de Ville, una pÃ©rfida mujer que vive en una gran mansiÃ³n y adora los abrigos de pieles, se entera de que los protagonistas tienen quince cachorros dÃ¡lmatas. Entonces, la idea de secuestrarlos para hacerse un exclusivo abrigo de pieles se convierte en una obsesiÃ³n enfermiza. Para hacer realidad su sueÃ±o contrata a dos ladrones.</p>

    patron = "<!-- SINOPSIS --> "
    patron += "<h2>[^<]+</h2> "
    patron += "<p>([^<]+)</p>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    plot = matches[0]

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron = '<tr>.*?'
    patron += '<td><img src="(.*?)".*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<a href="(.*?)".*?</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedidioma, scrapedcalidad, scrapedserver, scrapedurl in matches:
        idioma =""
        if "/img/1.png" in scrapedidioma: idioma="Castellano"
        if "/img/2.png" in scrapedidioma: idioma="Latino"
        if "/img/3.png" in scrapedidioma: idioma="Subtitulado"
        title = item.title + " ["+scrapedcalidad+"][" + idioma + "][" + scrapedserver + "]"

        itemlist.append( Item(channel=__channel__, action="play", title=title, fulltitle=title , url=scrapedurl , thumbnail="" , plot=plot , show = item.show) )
    return itemlist	

def play(item):
    logger.info("[pelisadicto.py] play")

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist    
