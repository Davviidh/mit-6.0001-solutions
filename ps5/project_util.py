# Utility functions for 6.00

from html.parser import HTMLParser

HTML_ESCAPE_DECODE_TABLE = { 
    "#39"   : "'",
    "quot"  : "\"",
    "#34"   : "\"",
    "amp"   : "&",
    "#38"   : "&",
    "lt"    : "<",
    "#60"   : "<",
    "gt"    : ">",
    "#62"   : ">",
    "nbsp"  : " ",
    "#160"  : " "   
}


class _HTMLTextExtractor(HTMLParser):
    """Collect readable text while retaining the starter's line breaks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "br":
            self.parts.append("\n")
        elif tag == "p":
            self.parts.append("\n\n")

    def handle_startendtag(self, tag, attrs):
        if tag.lower() == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "table":
            self.parts.append("\n")
        elif tag in {"a", "td", "li", "div", "p"}:
            self.parts.append(" ")

def translate_html(html_fragment):
    """
    Translates an HTML fragment to plain text.
    """
    if html_fragment is None:
        return ""

    parser = _HTMLTextExtractor()
    parser.feed(str(html_fragment))
    parser.close()
    return "".join(parser.parts)

def unicode_to_ascii(s):
    """
    Retained for compatibility with the original helper module.

    Python 3 and Tkinter handle Unicode text directly, so converting it to
    ASCII would unnecessarily replace names and non-English text with '?'.
    """
    return s
