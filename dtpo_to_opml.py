# Build an OPML file suitable for import into Tinderbox
# Charles Turner
# 2010-04-12

from appscript import *
import re


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

def makeset(lst):
  return '; '.join(lst)

def authordate(name):
  r = re.search('^(\d+)-(\w+)\.', name)
  if (r != None):
    return r.group(1), r.group(2)
  else:
    return "", ""

def children(record):
  props = record.properties.get()
  nm = opmlify(props[k.name])   # If name needs opmlify
  print '<outline text="%s" dtname="%s"' % (nm, nm)
  ad = authordate(props[k.name])   # sure should need it here
  print 'idate="%s" author="%s"' % (ad[0], ad[1])
  print 'dthinkurl="x-devonthink-item://%s"' % props[k.uuid]
  print 'dthinktags="%s"' % opmlify(makeset(props[k.tags]))
  note_t = props[k.type]
  if ((note_t == k.text) or (note_t == k.rtf) or (note_t == k.rtfd)):
    print '_note="%s"' % opmlify(props[k.plain_text]),
  else:
    print '_note=""',
  kids = dtpo.get(record.children)
  if (kids != []):
    print '>'
    for j in kids:
      children(j)
    print '</outline>'
  else:
      print '/>'

dtpo = app('DEVONthink Pro.app')
selection = dtpo.selection.get()

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<opml version="1.0">'
print '<head><title>Scratch</title></head>'   # Tbox doesn't use this info
print '<body>'

for i in selection:
  children(i)

print '</body>'
print '</opml>'

