import urllib.request

def check_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
