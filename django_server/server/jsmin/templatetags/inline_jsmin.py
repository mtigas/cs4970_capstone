from django.template import Library, Node
from jsmin.jsmin import jsmin

register = Library()

class JSMinNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        output = self.nodelist.render(context)
        try:
            return jsmin(output)
        except:
            return output

def do_jsmin(parser, token):
    nodelist = parser.parse(('endjsmin',))
    parser.delete_first_token()
    return JSMinNode(nodelist)

register.tag('startjsmin', do_jsmin)
