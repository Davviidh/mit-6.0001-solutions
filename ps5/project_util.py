# Utility functions for 6.00

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

def translate_html(html_fragment):
    """
    Translates an HTML fragment to plain text.
    """
    txt = ""                 
    parser_reg = ""            
    parser_state = "TEXT"    
    
    for x in html_fragment:  
        parser_reg += x     
        if parser_state == "TEXT":   
            if x == '<':             
                parser_state = "TAG"
            elif x == '&':           
                parser_state = "ESCAPE"
            else:                    
                txt += x             
                parser_reg = ""      
        elif parser_state == "TAG":    
            if x == '>':               
                parser_state = "TEXT"
                tag = parser_reg               
                if tag[1:-1] == "br" or tag[1:4] == "br ":
                    txt += "\n"
                elif tag == "</table>":
                    txt += "\n"
                elif tag == "<p>":
                    txt += "\n\n"
                # FIX: Add a space after closing structural tags to stop words from smashing together
                elif tag in ["</a>", "</td>", "</li>", "</div>", "</p>"]:
                    txt += " "
                parser_reg = ""      
        elif parser_state == "ESCAPE": 
            if x == ';':               
                parser_state = "TEXT"
                esc = parser_reg[1:-1] 
                if esc in HTML_ESCAPE_DECODE_TABLE:  
                    txt += HTML_ESCAPE_DECODE_TABLE[esc]
                else:
                    txt += " "         
                parser_reg = ""      

    if isinstance(txt, str):
        txt = unicode_to_ascii(txt)
        
    return txt

def unicode_to_ascii(s):
    """
    Safely translates curly punctuation marks to clean ASCII equivalents
    before encoding to eliminate '?' marks in the display text.
    """
    # Swap out modern typography characters before they hit the strict ASCII encoder
    replacements = {
        '’': "'", '‘': "'",
        '“': '"', '”': '"',
        '–': '-', '—': '-',
        '…': '...'
    }
    for original, replacement in replacements.items():
        s = s.replace(original, replacement)
        
    return s.encode('ascii', 'replace').decode('ascii')