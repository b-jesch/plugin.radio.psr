import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import sys
from urllib.parse import parse_qsl, urlencode
import os

addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')
player = xbmc.Player()

streams = dict({'Radio PSR Live': ['http://psr.hoerradar.de/psr-live-mp3-hq', 'stream-tile-live.jpg'],
                'Oli.P 90er Mix': ['https://90s90s.hoerradar.de/90s90s-inthemix-mp3-hq', 'stream-tile-olip.jpg'],
                'Radio PSR Sommer Hits': ['http://psr.hoerradar.de/psr-sommerhits-mp3-hq', 'stream-tile-sommerhits.jpg'],
                'Radio PSR Strandbar': ['https://barbaradio.hoerradar.de/barbaradio-strandbar-mp3-hq', 'stream-tile-strandbar.jpg'],
                'Radio PSR Sommer Party': ['https://feierfreund.hoerradar.de/feierfreund-summerdance-mp3-hq', 'stream-tile-sommerparty.jpg'],
                'Radio PSR Deutschpop Nonstop': ['http://psr.hoerradar.de/psr-deutschpop-mp3-hq', 'stream-tile-deutschpop.jpg'],
                'Radio PSR 90er': ['http://psr.hoerradar.de/psr-90er-mp3-hq', 'stream-tile-90er.jpg'],
                'Radio PSR 90er Dance': ['https://psr.hoerradar.de/psr-90er-dance-mp3-hq', 'stream-tile-90er-dance.jpg'],
                'Radio PSR 80er': ['http://psr.hoerradar.de/psr-80er-mp3-hq', 'stream-tile-80er.jpg'],
                'Radio PSR Chartbreaker': ['http://psr.hoerradar.de/psr-chartbreaker-mp3-hq', 'stream-tile-chartbreaker.jpg'],
                'Radio PSR Partymix': ['http://psr.hoerradar.de/psr-partymix-mp3-hq', 'stream-tile-partymix.jpg'],
                'Radio PSR Sachsensongs': ['http://psr.hoerradar.de/psr-sachsensongs-mp3-mq', 'stream-tile-sachsensongs.jpg'],
                'Radio PSR Sinnlos Telefon': ['http://psr.hoerradar.de/psr-sinnlostelefon-mp3-hq', 'stream-tile-sinnlos-telefon.jpg'],
                'Radio PSR Kids': ['http://psr.hoerradar.de/psr-kids-mp3-hq', 'stream-tile-kids_oT.jpg'],
                'Radio PSR 2000er': ['https://psr.hoerradar.de/psr-2000er-mp3-hq', 'stream-tile-2000er.jpg'],
                'Barbara Schöneberger': ['https://barbaradio.hoerradar.de/barbaradio-live-mp3-hq', 'stream-tile-schoeneberger.jpg'],
                'Radio PSR Relax': ['http://psr.hoerradar.de/psr-relax-mp3-hq', 'stream-tile-relax.jpg'],
                'Radio PSR Rock': ['http://psr.hoerradar.de/psr-rock-mp3-hq', 'stream-tile-rock.jpg']})


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
    if player.isPlaying():
        xbmc.log('Stop player')
        player.stop()
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
