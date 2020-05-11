import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urlparse import parse_qsl
from urllib import urlencode
import os

addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')

streams = dict({'PSR Live': ['http://psr.hoerradar.de/psr-live-mp3-hq', 'stream-tile-live.jpg'],
                'Deutschpop Nonstop': ['http://psr.hoerradar.de/psr-deutschpop-mp3-hq', 'stream-tile-deutschpop.jpg'],
                '90er': ['http://psr.hoerradar.de/psr-90er-mp3-hq', 'stream-tile-90er.jpg'],
                '80er': ['http://psr.hoerradar.de/psr-80er-mp3-hq', 'stream-tile-80er.jpg'],
                'Chartbreaker': ['http://psr.hoerradar.de/psr-chartbreaker-mp3-hq', 'stream-tile-chartbreaker.jpg'],
                'Partymix': ['http://psr.hoerradar.de/psr-partymix-mp3-hq', 'stream-tile-partymix.jpg'],
                'Sachsensongs': ['http://psr.hoerradar.de/psr-sachsensongs-mp3-mq', 'stream-tile-sachsensongs.jpg'],
                'Sinnlos Telefon': ['http://psr.hoerradar.de/psr-sinnlostelefon-mp3-hq', 'stream-tile-sinnlos-telefon.jpg'],
                'Kids': ['http://psr.hoerradar.de/psr-kids-mp3-hq', 'stream-tile-kids_oT.jpg'],
                'Relax': ['http://psr.hoerradar.de/psr-relax-mp3-hq', 'stream-tile-relax.jpg'],
                'Sommer Hits': ['http://psr.hoerradar.de/psr-sommerhits-mp3-hq', 'stream-tile-sommerhits.jpg'],
                'Rock': ['http://psr.hoerradar.de/psr-rock-mp3-hq', 'stream-tile-rock.jpg']})


def get_url(params):
    return '{0}?{1}'.format(_url, urlencode(params))


def get_image(image):
    return os.path.join(addonpath, 'resources', 'images', image)


def list_streams():
    xbmcplugin.setPluginCategory(_handle, 'Radio PSR Streams')
    xbmcplugin.setContent(_handle, 'songs')

    for stream in streams:
        liz = xbmcgui.ListItem(label=stream)
        liz.setPath(streams[stream][0])
        liz.setArt({'icon': get_image(streams[stream][1]), 'fanart': get_image('fanart.jpg')})
        liz.setProperty('IsPlayable', 'true')
        url = get_url({'action': 'play', 'url': streams[stream][0],
                       'icon': get_image(streams[stream][1]),
                       'title': 'Radio PSR \'{}\' Stream'.format(stream)})
        xbmcplugin.addDirectoryItem(_handle, url, liz, isFolder=False)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_stream(path, icon, title):
    xbmc.log('Playing {}'.format(path))
    play_item = xbmcgui.ListItem(path=path)
    play_item.setInfo('music', {'title': title})
    play_item.setArt({'icon': icon, 'thumb': icon, 'fanart': get_image('fanart.jpg')})
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(route):
    params = dict(parse_qsl(route))
    xbmc.log('Parameter list: {}'.format(params), xbmc.LOGDEBUG)
    if params:
        if params['action'] == 'play':
            play_stream(params['url'], params['icon'], params['title'])
    else:
        list_streams()


_url = sys.argv[0]
_handle = int(sys.argv[1])

if __name__ == '__main__':
    try:
        router(sys.argv[2][1:])
    except IndexError:
        pass
