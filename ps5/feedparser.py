import urllib.request
import xml.etree.ElementTree as ET
import ssl
from pathlib import Path


NETWORK_TIMEOUT = 15
SYSTEM_CA_FILES = (
    Path("/etc/ssl/cert.pem"),
    Path("/private/etc/ssl/cert.pem"),
)


def _create_verified_ssl_context():
    """Return a verified TLS context, including Python.org macOS installs.

    Python.org's macOS interpreter can be installed without its optional
    certificate-linking step. In that case OpenSSL reports no default CA file,
    even though macOS provides a current CA bundle at /etc/ssl/cert.pem.
    """
    verify_paths = ssl.get_default_verify_paths()
    if verify_paths.cafile or verify_paths.capath:
        return ssl.create_default_context()

    for ca_file in SYSTEM_CA_FILES:
        if ca_file.is_file():
            return ssl.create_default_context(cafile=str(ca_file))

    # Keep certificate verification enabled. If this context has no trust
    # anchors, urlopen will raise a useful verification error instead of
    # silently accepting an untrusted connection.
    return ssl.create_default_context()

class FeedParserDict(dict):
    """Custom dictionary subclass allowing both key and attribute access."""
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return ''
    def __setattr__(self, key, value):
        self[key] = value

def parse(url_or_file):
    """Parses RSS or Atom feeds cleanly in Python 3 without legacy cgi or sgmllib dependencies."""
    res = FeedParserDict()
    res.entries = []
    
    try:
        # Check if the input is a web URL
        if isinstance(url_or_file, str) and (url_or_file.startswith('http://') or url_or_file.startswith('https://')):
            req = urllib.request.Request(
                url_or_file, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            )
            context = _create_verified_ssl_context()
            with urllib.request.urlopen(
                req, context=context, timeout=NETWORK_TIMEOUT
            ) as response:
                xml_data = response.read()
        else:
            # Handle local file stream or path
            if hasattr(url_or_file, 'read'):
                xml_data = url_or_file.read()
            else:
                with open(url_or_file, 'rb') as f:
                    xml_data = f.read()
                    
        root = ET.fromstring(xml_data)
        
        # Look for RSS items
        items = root.findall('.//item')
        if items:
            for item in items:
                entry = FeedParserDict()
                entry.guid = item.findtext('guid') or item.findtext('link') or ''
                entry.title = item.findtext('title') or ''
                entry.link = item.findtext('link') or ''
                entry.description = item.findtext('description') or ''
                entry.published = item.findtext('pubDate') or item.findtext('pubdate') or ''
                res.entries.append(entry)
        else:
            # Fallback for Atom feed tags
            ns = {'a': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('.//a:entry', ns) or root.findall('.//entry')
            for item in entries:
                entry = FeedParserDict()
                entry.guid = item.findtext('a:id', namespaces=ns) or item.findtext('id') or ''
                entry.title = item.findtext('a:title', namespaces=ns) or item.findtext('title') or ''
                
                link_el = item.find('a:link', ns)
                if link_el is None:
                    link_el = item.find('link')
                entry.link = link_el.attrib.get('href', '') if link_el is not None else ''
                    
                entry.description = (item.findtext('a:summary', namespaces=ns) or 
                                     item.findtext('a:content', namespaces=ns) or 
                                     item.findtext('summary') or 
                                     item.findtext('content') or '')
                
                entry.published = (item.findtext('a:updated', namespaces=ns) or 
                                   item.findtext('a:published', namespaces=ns) or 
                                   item.findtext('updated') or 
                                   item.findtext('published') or '')
                res.entries.append(entry)
                
    except Exception as e:
        print(f"\n[FeedParser Error] Could not read/parse feed: {e}")
        
    return res
