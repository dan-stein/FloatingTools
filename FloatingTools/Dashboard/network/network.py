"""
Network class for Dashboard
"""
# ft imports
import FloatingTools
from FloatingTools.Dashboard import SERVER, dashboardEnv, ErrorPage, SITE_ENV
from FloatingTools.Dashboard.ui import *

# package imports
from flask import request, render_template_string, jsonify

# python imports
import re
import time
import socket
import urllib2
import traceback
import threading
from json import loads
from getpass import getuser
from subprocess import check_output


__all__ = [
    'refreshPeers'
]

# globals
IP_EXP = re.compile("([0-9]+.[0-9]+.[0-9].[0-9]+)")

# Host ip
HOST = socket.gethostbyname(socket.gethostname())
SITE_ENV['ft_peers'] = {}


@SERVER.route('/_receiving')
def receive():
    """
    -- private --
    """
    try:
        sender = request.args['from']
        # handlerType = request.args['type']
        # handlerName = request.args['handler']

        handlerType = 'App'
        handlerName = 'Blur'

        data = {}

        for var in request.args:
            if var not in ['type', 'handler']:
                data[var] = request.args[var]

        handler = None
        if handlerType == 'App':
            handler = FloatingTools.App.APPS[handlerName]
        if handlerType == 'AbstractApplication':
            handler = FloatingTools.wrapper()


        p = Page('Receiving Center')
        p.add(Element('center', value=Element('h2', value='Message received!')))
        p.addDivider()
        p.add(Element('center', value='Handler Type: ' + handlerType))
        p.addBreak()
        p.add(Element('center', value='Handler: ' + handlerName))
        p.addBreak()
        p.add(Element('center', value='Data: ' + str(data)))

        return render_template_string(p.render(), **dashboardEnv())

    except Exception, e:
        return render_template_string(ErrorPage(errorType=e, traceback=traceback.format_exc()).render(), **dashboardEnv())


@SERVER.route('/_identify')
def _respond():
    data = {
        'user': getuser(),
        'host': HOST,
        'application': FloatingTools.wrapperName()
    }
    return jsonify(data)


def pingIP(ip):
    response = urllib2.urlopen('http://%(ip)s:5000/_identify' % locals())
    return loads(response.read())


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

    for ip in ips:
        try:
            urllib2.urlopen('http://%(ip)s:5000/_identify' % locals(), timeout=.1)
            SITE_ENV['ft_peers'][ip] = pingIP(ip)
            FloatingTools.FT_LOOGER.debug('Found peer! ' + 'http://%(ip)s:5000' % locals())
        except (urllib2.URLError, socket.timeout):
            continue


def refreshPeers():
    threading.Thread(target=_pullPeers).start()

try:
    refreshPeers()
except:
    FloatingTools.FT_LOOGER.warning('Networking capabilities failed to initialize.')
    traceback.print_exc()