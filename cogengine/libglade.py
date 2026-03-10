# Compatibility shim: the old standalone libglade module is now part of gtk.glade
import gtk.glade as _glade

GladeXML = _glade.XML
