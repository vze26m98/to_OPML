#! /usr/local/bin/python

# Build an OPML file suitable for import into Tinderbox
# Charles Turner
# 2010-09-10

from appscript import *
import re, codecs, os


def escape(m):
  if (m.group(0) == '"'):
    return '&quot;'
  elif (m.group(0) == '\t'):
    return '&#9;'
  elif (m.group(0) == '\n'):
    return '&#10;'
  elif (m.group(0) == '>'):
    return '&gt;'
  elif (m.group(0) == '<'):
    return '&lt;'
  elif (m.group(0) == '&'):
    return '&amp;'

def opmlify(txt):
  return re.sub('(")|(\t)|(\n)|(>)|(<)|(&)', escape, txt)

def children(record):
  pg = opmlify(record.page.label.get())   # If name needs opmlify
  global text, name
  text += '<outline text="page %s" Prototype="%s" DisplayExpression="$Prototype + \' : \' + $Name" ' % (pg, name)
  text += '_note="%s"' % opmlify(record.text.get())
  text +=  '/>\n'

skim = app('Skim.app')
name = skim.documents[1].name.get()
notes = skim.documents[1].notes.get()

fd = codecs.open(os.environ['HOME'] + '/Desktop/' + name[:-4] + '.opml', 'w', 'utf-8')

text = '<?xml version="1.0" encoding="UTF-8"?>\n'
text += '<opml version="1.0">\n'
text += '<head><title>Scratch</title></head>\n'   # Tbox doesn't use this info
text += '<body>\n'
text += '<outline text="%s" IsPrototype="true" PrototypeBequeathsChildren="false">\n' % (name)

for i in notes:
  children(i)

text += '</outline>\n'
text += '</body>\n'
text += '</opml>\n'

fd.write(text)
fd.close()
