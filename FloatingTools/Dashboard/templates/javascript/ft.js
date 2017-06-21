function refreshPeers() {
    var current = window.location.pathname;
    document.location.href = "/_refreshPeers?source=" + current;
}

function downloadFromPeer(peer) {
    var current = window.location.pathname;
    document.location.href = "/_retrieve?source=" + current + "&ip=" + peer;
}

function appPassArgs(app, func, args, elements) {
    path = app + '/' + func + '?sourcePage=' + window.location.pathname + '&';
    var addAnd = false;

    for (x in args) {
        if (addAnd == true) {
            path += '&'
        }
        path += x + '=' + args[x];
        addAnd = true;
    }

    for (x in elements) {
        if (addAnd == true) {
            path += '&'
        }
        path += x + '=' + document.getElementById(elements[x]).value;
        addAnd = true;
    }

    document.location.href = path;
}