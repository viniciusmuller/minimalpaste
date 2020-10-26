import html


with open("templates/template.html", 'r', encoding="utf-8") as f:
    TEMPLATE_HTML = f.read()

# Minified form containing a textarea for user input 
FORM = ('<form action="/paste" id="paste" method="POST" onsubmit="return '
        'validatePaste()";><textarea name="new_paste_content" spellcheck="fals'
        'e" cols="90" rows="35" onkeydown="if(event.keyCode===9){var v=this.va'
        'lue,s=this.selectionStart,e=this.selectionEnd;this.value=v.substring('
        '0, s)+"\t"+v.substring(e);this.selectionStart=this.selectionEnd=s+1;r'
        'eturn false;}"></textarea></form>')

HOME_BUTTON = '<a href="/"><button class="button uns">Home</button></a>\n'
FORM_BUTTON = '<button class="button uns" form="paste">Paste!</button></a>\n'


def sanitize_content(content: str, /) -> str:
    """
    Sanitize paste content to prevent XSS attacks.

    Parameter
    ---------
    content: `str`
        Content to be sanitized.

    Returns
    -------
    sanitized : `str`
        Same string containing the html entities encoded.
    """
    return html.escape(content)


def create_template(content: str = '', /) -> str:
    """
    Receives a content string, sanitizes and build a HTML page.

    Parameter
    ---------
    content : `str`
        String containing the user paste content.

    Returns
    -------
    template : `str`
        HTML template containing the paste content in a pre tag
        if it was supplied else a POST form containing an textarea.
    """
    sanitized = sanitize_content(content)

    if content:
        pre_tag = f"<pre>\n{sanitized}\n</pre>"
        return TEMPLATE_HTML.replace("{%}", HOME_BUTTON + pre_tag)
    else:
        return TEMPLATE_HTML.replace("{%}", FORM_BUTTON + FORM)
