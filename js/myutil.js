
function foreach(a, func) {
    if (a instanceof Array) {
        for (var i = 0; i < a.length; i++) {
            if (func(a[i], i) == false) break
        }
    } else {
        for (var k in a) {
            if (a.hasOwnProperty(k)) {
                if (func(a[k], k) == false) break
            }
        }
    }
    return a
}

function getURLParams(url) {
    if (url === undefined)
        url = window.location.href
    var start = url.indexOf("?")
    if (start < 0)
        return {}
    var pound = url.indexOf("#")
    url = url.slice(start + 1, pound >= 0 ? pound : url.length)
    var hash = {}
    foreach(url.split(/&/), function (pair) {
        var equals = pair.indexOf("=")
        if (equals >= 0)
            hash[decodeURI(pair.slice(0, equals))] = decodeURI(pair.slice(equals + 1))
        else
            hash[decodeURI(pair)] = true
    })
    return hash
}
getUrlParams = getURLParams

function time() {
    return new Date().getTime()
}

