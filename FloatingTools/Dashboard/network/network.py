"""
Network class for Dashboard
"""
# ft imports
import FloatingTools
from FloatingTools.Dashboard import SERVER, SITE_ENV, HOST

# package imports
from flask import request, jsonify, redirect

# python imports
import re
import time
import socket
import urllib2
import threading
from json import loads
from getpass import getuser
from subprocess import check_output


__all__ = [
    'refreshPeers',
    'peers',
    'pingIP',
    'send'
]

# globals
IP_EXP = re.compile("([0-9]+.[0-9]+.[0-9].[0-9]+)")

# Host ip
SITE_ENV['ft_peers'] = {}

# Out going data
OUT_GOING = None

def send(data, ip):
    """
Send data to a peer.

:param data:
:param ip:
    """
    # store data
    global OUT_GOING
    OUT_GOING = {ip: data}


@SERVER.route('/_retrieve')
def _retrieve():
    ip = request.args['ip']
    outBoxData = FloatingTools.Dashboard.pingIP(ip)[u'outBox']

    if 'type' not in outBoxData and 'target' not in outBoxData:
        FloatingTools.FT_LOOGER.error('Data passed was not valid. Must specify the type of data being passed (App, '
                                      'Wrapper, etc...) and what the target it is (the name of the type that you are '
                                      'sending the data to).')

    if outBoxData['type'] == 'App':
        FloatingTools.App.APPS[outBoxData['target']].receive(outBoxData['data'])
        urllib2.urlopen('http://%(ip)s:5000/_pickedUp' % locals())

    FloatingTools.Dashboard.refreshPeers()

    return redirect(request.args['source'])


@SERVER.route('/_pickedUp')
def _pickedUp():
    # reset data
    global OUT_GOING
    OUT_GOING = None

    return ''


@SERVER.route('/_identify')
def _respond():

    outData = None

    if OUT_GOING:
        try:
            outData = OUT_GOING[request.remote_addr]
        except KeyError:
            pass

    data = {
        'user': getuser(),
        'host': HOST,
        'application': FloatingTools.wrapperName(),
        'address': 'http://%s:5000/' % HOST,
        'hasData': True if outData else False,
        'outBox': outData
    }

    return jsonify(data)


def pingIP(ip):
    response = urllib2.urlopen('http://%(ip)s:5000/_identify' % locals())
    return loads(response.read())


def peers():
    return SITE_ENV['ft_peers']


def _pullPeers():
    """
Refresh the network for new peer list and updated snapshot of enabled Dashboard users.
    """
    SITE_ENV['ft_peers'] = {}

    start = time.time()
    result = check_output(['arp', '-a'])
    end = time.time()

    ips = IP_EXP.findall(result)
    pingTime = end - start

    FloatingTools.FT_LOOGER.info('Network Ping took: {:.6f} secs.'.format(pingTime))
    if pingTime > 2:
        FloatingTools.FT_LOOGER.info('Network ping times longer than usually 2 secs are attributed to slow network '
                                     'speeds, very large networks with lots of ip addresses or there are invalid ip '
                                     'addresses that are slow to respond as invalid. Usually a restart will help '
                                     'alleviate this problem.'.format(pingTime))

    if len(ips) > 20:
        FloatingTools.FT_LOOGER.warning(
            'Large network: %s addresses found.\nWorst case delay with 0.1 timeout: %s secs.' % (
                len(ips),
                .1*len(ips)
            )
        )

    hitIps = []
    for ip in ips:
        if ip in hitIps:
            continue
        hitIps.append(ip)
        try:
            urllib2.urlopen('http://%(ip)s:5000/_identify' % locals(), timeout=.1)
            SITE_ENV['ft_peers'][ip] = pingIP(ip)
            FloatingTools.FT_LOOGER.debug('Found peer! ' + 'http://%(ip)s:5000' % locals())
        except (urllib2.URLError, socket.timeout):
            continue


def refreshPeers(threaded=False):
    if threaded:
        threading.Thread(target=_pullPeers).start()
    else:
        _pullPeers()


@SERVER.route('/_refreshPeers')
def _refresh():
    _pullPeers()
    return redirect(request.args['source'])