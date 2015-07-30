# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasdk
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__category__ = "F"
__language__ = "ES"
__title__ = "PeliculasDK"
__fanart__ = ""
__type__ = "generic"
__disabled__ = False
__version__ = 1
__adult__ = False
__date__ = "12/05/2015"
__creationdate__ = ""
__changes__ = "peliculasdk: correccion enlaces, añadidos arts"
__thumbnail__ = "http://s29.postimg.org/wzw749oon/pldklog.jpg"
__channel__ = "peliculasdk"

import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools
try:
    import xbmc
    import xbmcgui
except: pass

DEBUG = config.get_setting("debug")

host = "http://www.peliculasdk.com/"
fanart = ""

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.peliculasdk mainlist")
    itemlist = []
    title ="Estrenos"
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, title=title      , action="peliculas", url="http://www.peliculasdk.com/ver/estrenos", fanart="http://s24.postimg.org/z6ulldcph/pdkesfan.jpg", thumbnail="http://s16.postimg.org/st4x601d1/pdkesth.jpg"))
    title ="PelisHd"
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, title=title     , action="peliculas", url="http://www.peliculasdk.com/calidad/HD-720/", fanart="http://s18.postimg.org/wzqonq3w9/pdkhdfan.jpg", thumbnail="http://s8.postimg.org/nn5669ln9/pdkhdthu.jpg"))
    title ="Pelis HD-Rip"
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, title=title      , action="peliculas", url="http://www.peliculasdk.com/calidad/HD-320", fanart="http://s7.postimg.org/3pmnrnu7f/pdkripfan.jpg", thumbnail="http://s12.postimg.org/r7re8fie5/pdkhdripthub.jpg"))
    title ="Pelis Audio español"
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, title=title     , action="peliculas", url="http://www.peliculasdk.com/idioma/Espanol/", fanart="http://s11.postimg.org/65t7bxlzn/pdkespfan.jpg", thumbnail="http://s13.postimg.org/sh1034ign/pdkhsphtub.jpg"))
    title ="Buscar..."
    title = title.replace(title,"[COLOR orange]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, title=title      , action="search", url="http://www.peliculasdk.com/calidad/HD-720/", fanart="http://s14.postimg.org/ceqajaw2p/pdkbusfan.jpg", thumbnail="http://s13.postimg.org/o85gsftyv/pdkbusthub.jpg"))
    

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.peliculasdk search")
    texto = texto.replace(" ","+")
    
    item.url = "http://www.peliculasdk.com/index.php?s=%s&x=0&y=0" % (texto)
    
    try:
        return buscador(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.peliculasdk buscador")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)


    patron = 'style="width:100;height:140px; ">'
    patron += '<a href="([^"]+)".*?'
    patron += 'title="([^<]+)">.*?'
    patron += 'src="([^"]+)".*?'
    patron += '<span class="clms2">Audio.*?rel="tag">([^"]+)</a>.*?'
    patron += '<span class="clms2">Calidad.*?rel="tag">([^"]+)</a>'
    

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
        itemlist.append( Item(channel=__channel__, title="[COLOR gold][B]Sin resultados...[/B][/COLOR]", thumbnail ="http://s6.postimg.org/t8gfes7rl/pdknoisethumb.png", fanart ="http://s6.postimg.org/oy1rj72oh/pdknoisefan.jpg",folder=False) )

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedlenguaje, scrapedcalidad in matches:
        scrapedcalidad = scrapedcalidad.replace(scrapedcalidad,"[COLOR orange]"+scrapedcalidad+"[/COLOR]")
        scrapedlenguaje = scrapedlenguaje.replace(scrapedlenguaje,"[COLOR orange]"+scrapedlenguaje+"[/COLOR]")
        scrapedtitle = scrapedtitle + "-(Idioma: " + scrapedlenguaje + ")" + "-(Calidad: " + scrapedcalidad +")"
        scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart="http://s18.postimg.org/h9kb22mnt/pdkfanart.jpg", folder=True) )

    return itemlist




def peliculas(item):
    logger.info("pelisalacarta.peliculasdk peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&#.*?;","",data)
    
    
    


    patron = 'style="position:relative;"> '
    patron += '<a href="([^"]+)" '
    patron += 'title="([^<]+)">'
    patron += '<img src="([^"]+)".*?'
    patron += 'rel="tag">([^"]+)</a>'
    patron += '</br>Calidad.*?rel="tag">([^"]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)


    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedlenguaje, scrapedcalidad in matches:
        scrapedcalidad = scrapedcalidad.replace(scrapedcalidad,"[COLOR orange]"+scrapedcalidad+"[/COLOR]")
        scrapedlenguaje = scrapedlenguaje.replace(scrapedlenguaje,"[COLOR orange]"+scrapedlenguaje+"[/COLOR]")
        scrapedtitle = scrapedtitle + "-(Idioma: " + scrapedlenguaje + ")" + "-(Calidad: " + scrapedcalidad +")"
        scrapedtitle = scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action="fanart", thumbnail=scrapedthumbnail, fanart="http://s18.postimg.org/h9kb22mnt/pdkfanart.jpg", folder=True) )
    ## Paginación
    patronvideos  = '<a href="([^"]+)" >Siguiente &raquo;</a></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        title ="siguiente>>"
        title = title.replace(title,"[COLOR red]"+title+"[/COLOR]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=scrapedurl , thumbnail="http://s6.postimg.org/uej03x4r5/bricoflecha.png", fanart="http://s18.postimg.org/h9kb22mnt/pdkfanart.jpg",  folder=True) )
    

    return itemlist

def fanart(item):
    logger.info("pelisalacarta.peliculasdk fanart")
    itemlist = []
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    title= scrapertools.get_match(data,'<div id="titleopcions">Ver película(.*?)\(')
    title= re.sub(r"3D|SBS|-|","",title)
    title= title.replace('á','a')
    title= title.replace('Á','A')
    title= title.replace('é','e')
    title= title.replace('í','i')
    title= title.replace('ó','o')
    title= title.replace('ú','u')
    title= title.replace('ñ','n')
    title= title.replace('Crepusculo','Twilight')
    title= title.replace(' ','%20')
    url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id":(.*?),"original_title"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        extra=item.thumbnail
        show= item.thumbnail
        category= item.thumbnail
        itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail ,extra=extra, show=show, category= category, folder=True) )
    else:
        for fan, id in matches:
            fanart="https://image.tmdb.org/t/p/original" + fan
            item.extra= fanart
    #fanart_2 y arts
                
            url ="http://assets.fanart.tv/v3/movies/"+id+"?api_key=6fa42b0ef3b5f3aab6a7edaa78675ac2"
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"hdmovielogo":.*?"url": "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if '"moviedisc"' in data:
                disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
            if '"movieposter"' in data:
                poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
            if '"moviethumb"' in data:
                thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
            if '"moviebanner"' in data:
                 banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
        
            if len(matches)==0:
               extra=  item.thumbnail
               show = item.extra
               category = item.extra
               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra,  extra=extra, show=show, category= category, folder=True) )
        for logo in matches:
            if '"hdmovieclearart"' in data:
                clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                if '"moviebackground"' in data:
                     fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                     extra=clear
                     show= fanart_2
                     if '"moviedisc"' in data:
                        category= disc
                     else:
                         category= clear
                     itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category, folder=True) )
                else:
                    extra= clear
                    show=item.extra
                    if '"moviedisc"' in data:
                       category = disc
                    else:
                        category = clear
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category, folder=True) )
                
            if '"moviebackground"' in data:
                fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                if '"hdmovieclearart"' in data:
                    clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                    extra=clear
                    show= fanart_2
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                        category= clear
                    
                else:
                    extra=logo
                    show= fanart_2
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                        category= logo
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category,  folder=True) )

            if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                    extra= logo
                    show=  item.extra
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                         category= item.extra
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra,category= category, extra=extra,show=show ,  folder=True) )
    
    title ="Info"
    if len(item.extra)==0:
        fanart=item.thumbnail
    else:
        fanart = item.extra

    if '"movieposter"' in data:
         thumbnail= poster

    else:
        thumbnail = item.thumbnail
    title = title.replace(title,"[COLOR skyblue]"+title+"[/COLOR]")
    itemlist.append( Item(channel=__channel__, action="info" , title=title , url=item.url, thumbnail=thumbnail, fanart=fanart, extra = extra, show = show,folder=False ))


    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.peliculasdk findvideos")
    
    itemlist = []
    data = re.sub(r"<!--.*?-->","",scrapertools.cache_page(item.url))
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    
    servers_data_list = {}
    patron = '<div id="tab\d+" class="tab_content"><script>(\w+)\("([^"]+)"\)</script></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for server, id in matches:
        scrapedplot = scrapertools.get_match(data,'<span class="clms">(.*?)</div></div>')
        plotformat = re.compile('(.*?:) </span>',re.DOTALL).findall(scrapedplot)
        scrapedplot = scrapedplot.replace(scrapedplot,"[COLOR white]"+scrapedplot+"[/COLOR]")
        
        for plot in plotformat:
            scrapedplot = scrapedplot.replace(plot,"[COLOR red][B]"+plot+"[/B][/COLOR]")
        scrapedplot = scrapedplot.replace("</span>","[CR]")
        scrapedplot = scrapedplot.replace(":","")
        servers_data_list.update({server:id})
    
    url = "http://www.peliculasdk.com/Js/videos.js"
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    patron = 'function (\w+)\(id\).*?'
    patron+= 'data-src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for server, url in matches:
        

        if server in servers_data_list:
            video_url = re.sub(r"embed\-|\-630x400\.html","",url)
            video_url = video_url.replace("'+codigo+'",servers_data_list[server])
            servertitle = scrapertools.get_match(video_url,'http://(.*?)/')
            servertitle = servertitle.replace(servertitle,"[COLOR red]"+servertitle+"[/COLOR]")
            servertitle = servertitle.replace("embed.","")
            servertitle = servertitle.replace("player.","")
            servertitle = servertitle.replace("api.video.","")
            servertitle = servertitle.replace("hqq.tv","netu.tv")
            title = "[COLOR orange]Ver en --[/COLOR]" + servertitle
            itemlist.append( Item(channel=__channel__, title =title , url=video_url, action="play", thumbnail=item.category, plot=scrapedplot, fanart=item.show ) )

    return itemlist


def play(item):
    logger.info("pelisalacarta.bricocine findvideos")
    
    itemlist = servertools.find_video_items(data=item.url)
    data = scrapertools.cache_page(item.url)
    
    
    
    listavideos = servertools.findvideos(data)
    
    for video in listavideos:
        videotitle = scrapertools.unescape(video[0])
        url =item.url
        server = video[2]
        
        #xbmctools.addnewvideo( __channel__ , "play" , category , server ,  , url , thumbnail , plot )
        itemlist.append( Item(channel=__channel__, action="play", server=server, title="Trailer - " + videotitle  , url=url , thumbnail=item.thumbnail , plot=item.plot , fulltitle = item.title , fanart="http://s23.postimg.org/84vkeq863/movietrailers.jpg", folder=False) )
    
    
   

    return itemlist

def info(item):
    logger.info("pelisalacarta.zentorrents info")
    
    url=item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    title= scrapertools.get_match(data,'<div id="titleopcions">Ver película(.*?)\(')
    title = title.replace(title,"[COLOR aqua][B]"+title+"[/B][/COLOR]")
    plot = scrapertools.get_match(data,'<span class="clms">(.*?)</div></div>')
    plotformat = re.compile('(.*?:) </span>',re.DOTALL).findall(plot)
    plot = plot.replace(plot,"[COLOR white]"+plot+"[/COLOR]")
    for info in plotformat:
        plot = plot.replace(info,"[COLOR red][B]"+info+"[/B][/COLOR]")
    plot = plot.replace("</span>","[CR]")
    plot = plot.replace(":","")
    foto = item.show
    photo= item.extra

    ventana2 = TextBox1(title=title, plot=plot, thumbnail=photo, fanart=foto)
    ventana2.doModal()

class TextBox1( xbmcgui.WindowDialog ):
        """ Create a skinned textbox window """
        def __init__( self, *args, **kwargs):
            
            self.getTitle = kwargs.get('title')
            self.getPlot = kwargs.get('plot')
            self.getThumbnail = kwargs.get('thumbnail')
            self.getFanart = kwargs.get('fanart')
            
            self.background = xbmcgui.ControlImage( 70, 20, 1150, 630, 'http://s6.postimg.org/58jknrvtd/backgroundventana5.png')
            self.title = xbmcgui.ControlTextBox(140, 60, 1130, 50)
            self.plot = xbmcgui.ControlTextBox( 140, 140, 1035, 600 )
            self.thumbnail = xbmcgui.ControlImage( 813, 43, 390, 100, self.getThumbnail )
            self.fanart = xbmcgui.ControlImage( 140, 351, 1035, 250, self.getFanart )
            
            self.addControl(self.background)
            self.addControl(self.title)
            self.addControl(self.plot)
            self.addControl(self.thumbnail)
            self.addControl(self.fanart)
            
            self.title.setText( self.getTitle )
            self.plot.setText(  self.getPlot )
        
        def get(self):
            self.show()
        
        def onAction(self, action):
            self.close()

def test():
    return True



