import upnpclient
import xml.etree.ElementTree as ET

def parse_dlna():
    """
    Return a dict of title: url from dlna
    """
    res = [
        s for s in  upnpclient.Device("http://127.0.0.1:8200/rootDesc.xml").services
        if s.name == 'ContentDirectory'
    ][0].Browse(
        ObjectID="2$8", BrowseFlag="BrowseDirectChildren", Filter="", StartingIndex=0,
        RequestedCount=100000, SortCriteria=""
    )['Result']

    root = ET.fromstring(res)

    return {item[0].text: item[3].text for item in root}
