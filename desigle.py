#!/usr/bin/env python

#    DeSiGLE
#    Copyright (C) 2008 Derek Anderson
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import commands, dircache, getopt, math, os, re, string, sys, tempfile, thread, threading, time, traceback
from datetime import date, datetime, timedelta
from latex_tags import *

RUN_FROM_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
CURRENT_DIR = os.path.expanduser("~")
PROGRAM = 'DeSiGLE'
SVN_INFO = commands.getoutput('svn info')
VERSION = ''
for line in SVN_INFO.split('\n'):
    if line.startswith('Revision:'):
        VERSION = 'svn:'+ line[10:]

GPL = open( RUN_FROM_DIR + 'GPL.txt', 'r' ).read()

# GUI imports
try:
    import pygtk
    pygtk.require("2.0")
    import gobject
    import gtkspell 
    import gtk
    import gtk.glade
    import gnome
    import gnome.ui
    import pango
    gobject.threads_init()
    gtk.gdk.threads_init()
except:
    traceback.print_exc()
    print 'could not import required GTK libraries.  try running:'
    print '\tfor ubuntu: sudo apt-get install python python-glade2 python-gnome2 python-gconf python-gnome2-extras'
    print '\tfor debian: sudo apt-get install python python-glade2 python-gnome2 python-gnome2-extras'
    print '\tfor redhat: yum install pygtk2 gnome-python2-gconf pygtk2-libglade python-gnome2-extras'
    sys.exit()

try:
    import poppler
except:
    traceback.print_exc()
    print 'could not import python-poppler [https://code.launchpad.net/~poppler-python/poppler-python/].  try running (from "%s"):' % RUN_FROM_DIR
    print "\tsudo apt-get install build-essential libpoppler2 libpoppler-dev libpoppler-glib2 libpoppler-glib-dev python-cairo-dev bzr gnome-common python-dev python-gnome2-dev python-gtk2-dev python-gobject-dev python-pyorbit-dev"
    print '\tbzr branch http://bazaar.launchpad.net/~poppler-python/poppler-python/poppler-0.6-experimental'
    print '\tcd poppler-0.6-experimental'
    print '\t./autogen.sh'
    print '\t./configure'
    print '\tmake'
    print '\tsudo make install'
    sys.exit()



class MainGUI:

    current_file = None
    changed_time = None
    changed = False

    def __init__(self):
        gnome.init(PROGRAM, VERSION)
        self.ui = gtk.glade.XML(RUN_FROM_DIR + 'desigle.glade')
        self.main_window = self.ui.get_widget('desigle')
        self.main_window.connect("delete-event", lambda x,y: self.exit() )
        
        self.init_menu()
        self.init_editor()
        self.init_tags()
        self.init_pdf_preview_pane()

        thread.start_new_thread( self.watch_editor, () )

        self.main_window.show()
        
        
    def init_menu(self):
        self.ui.get_widget('menu_new').connect('activate', lambda x: self.new())
        self.ui.get_widget('menu_open').connect('activate', lambda x: self.open())
        self.ui.get_widget('menu_save').connect('activate', lambda x: self.save())
        self.ui.get_widget('menu_save_as').connect('activate', lambda x: self.save_as())
        self.ui.get_widget('menu_quit').connect('activate', lambda x: self.exit())
        
        self.ui.get_widget('menu_save').set_sensitive( self.current_file!=None )
        
        self.ui.get_widget('toolbutton_new').connect('clicked', lambda x: self.new())
        self.ui.get_widget('toolbutton_open').connect('clicked', lambda x: self.open())
        self.ui.get_widget('toolbutton_save').connect('clicked', lambda x: self.save())

        self.ui.get_widget('toolbutton_save').set_sensitive( self.current_file!=None )

        
    def init_editor(self):
        self.editor = self.ui.get_widget('editor')
        pangoFont = pango.FontDescription('monospace')
        self.editor.modify_font(pangoFont)
        self.ui.get_widget('textview_output').modify_font(pangoFont)
        spell = gtkspell.Spell(self.editor)
        spell.set_language("en_US")
        self.editor.get_buffer().connect('changed', self.editor_text_change_event )
        self.editor.get_buffer().connect('mark-set', self.editor_mark_set_event )
        
    
    def editor_text_change_event(self, buffer):
        self.changed_time = datetime.now()
        if not self.changed: self.main_window.set_title( self.main_window.get_title()+'*' )
        self.changed = True
#        iter=buffer.get_iter_at_mark(buffer.get_insert())
#        start = buffer.get_iter_at_line( iter.get_line() )
#        end = buffer.get_iter_at_line( iter.get_line()+1 )
#        if iter.get_line()>=buffer.get_line_count()-1:
#            end = buffer.get_end_iter()
#        self.retag( buffer, start, end )


    def editor_mark_set_event(self, buffer, x, y):
        iter=buffer.get_iter_at_mark(buffer.get_insert())
        self.ui.get_widget('label_row_col').set_text( 'line:%i/%i col:%i/%i' % ( iter.get_line(), buffer.get_line_count(), iter.get_line_offset(), iter.get_chars_in_line() ) )
        
    
    def init_tags(self):
        tag_table = self.editor.get_buffer().get_tag_table()
        for tag_name, tag_attr in LATEX_TAGS:
            warn_tag = gtk.TextTag(tag_name)
            for k,v in tag_attr['properties'].iteritems():
                warn_tag.set_property(k,v)
            tag_table.add(warn_tag)
        
    
        
    def retag( self, buffer, start, end ):
        for tag_name, tag_attr in LATEX_TAGS:
            buffer.remove_tag_by_name(tag_name, start, end)
            p = tag_attr['regex']
            line = start.get_text(end)
            for match in p.finditer(line):
                st = buffer.get_iter_at_offset( start.get_offset()+ match.span()[0] )
                et = buffer.get_iter_at_offset( start.get_offset()+ match.span()[1] )
                buffer.apply_tag_by_name( tag_name, st, et )
        


    def init_pdf_preview_pane(self):
        file, self.tex_file = tempfile.mkstemp('.tex')
        self.pdf_file = self.tex_file[:-4]+'.pdf'
        print 'tex_file', self.tex_file
        print 'pdf_file', self.pdf_file

        pdf_preview = self.ui.get_widget('pdf_preview')
        self.pdf_preview = { 'current_page_number':0 }
        self.pdf_preview['scale'] = None
        pdf_preview.connect("expose-event", self.on_expose_pdf_preview)
        
        self.ui.get_widget('button_move_previous_page').connect('clicked', lambda x: self.goto_pdf_page( self.pdf_preview['current_page_number']-1 ) )
        self.ui.get_widget('button_move_next_page').connect('clicked', lambda x: self.goto_pdf_page( self.pdf_preview['current_page_number']+1 ) )
        self.ui.get_widget('button_zoom_in').connect('clicked', lambda x: self.zoom_pdf_page( -1.2 ) )
        self.ui.get_widget('button_zoom_out').connect('clicked', lambda x: self.zoom_pdf_page( -.8 ) )
        self.ui.get_widget('button_zoom_normal').connect('clicked', lambda x: self.zoom_pdf_page( 1 ) )
        self.ui.get_widget('button_zoom_best_fit').connect('clicked', lambda x: self.zoom_pdf_page( None ) )
        self.ui.get_widget('button_save_pdf').connect('clicked', lambda x: self.save_pdf() )

    def refresh_pdf_preview_pane(self):
        pdf_preview = self.ui.get_widget('pdf_preview')
        
        if os.path.isfile( self.pdf_file ):
            self.pdf_preview['document'] = poppler.document_new_from_file ('file://'+ self.pdf_file, None)
            self.pdf_preview['n_pages'] = self.pdf_preview['document'].get_n_pages()
            self.pdf_preview['scale'] = None
            self.goto_pdf_page( self.pdf_preview['current_page_number'], new_doc=True )
        else:
            pdf_preview.set_size_request(0,0)
            self.pdf_preview['current_page'] = None
            self.ui.get_widget('button_move_previous_page').set_sensitive( False )
            self.ui.get_widget('button_move_next_page').set_sensitive( False )
            self.ui.get_widget('button_zoom_out').set_sensitive( False )
            self.ui.get_widget('button_zoom_in').set_sensitive( False )
            self.ui.get_widget('button_zoom_normal').set_sensitive( False )
            self.ui.get_widget('button_zoom_best_fit').set_sensitive( False )
        pdf_preview.queue_draw()
        
    def goto_pdf_page(self, page_number, new_doc=False):
        if True:
            if not new_doc and self.pdf_preview.get('current_page') and self.pdf_preview['current_page_number']==page_number:
                return
            if page_number<0: page_number = 0
            pdf_preview = self.ui.get_widget('pdf_preview')
            self.pdf_preview['current_page_number'] = page_number
            self.pdf_preview['current_page'] = self.pdf_preview['document'].get_page( self.pdf_preview['current_page_number'] )
            if self.pdf_preview['current_page']:
                self.pdf_preview['width'], self.pdf_preview['height'] = self.pdf_preview['current_page'].get_size()
                self.ui.get_widget('button_move_previous_page').set_sensitive( page_number>0 )
                self.ui.get_widget('button_move_next_page').set_sensitive( page_number<self.pdf_preview['n_pages']-1 )
                self.zoom_pdf_page( self.pdf_preview['scale'], redraw=False )
            else:
                self.ui.get_widget('button_move_previous_page').set_sensitive( False )
                self.ui.get_widget('button_move_next_page').set_sensitive( False )
            pdf_preview.queue_draw()
        else:
            self.ui.get_widget('button_move_previous_page').set_sensitive( False )
            self.ui.get_widget('button_move_next_page').set_sensitive( False )

    def zoom_pdf_page(self, scale, redraw=True):
        """None==auto-size, negative means relative, positive means fixed"""
        if True:
            if redraw and self.pdf_preview.get('current_page') and self.pdf_preview['scale']==scale:
                return
            pdf_preview = self.ui.get_widget('pdf_preview')
            auto_scale = (pdf_preview.get_parent().get_allocation().width-2.0) / self.pdf_preview['width']
            if scale==None:
                scale = auto_scale
            else:
                if scale<0:
                    if self.pdf_preview['scale']==None: self.pdf_preview['scale'] = auto_scale
                    scale = self.pdf_preview['scale'] = self.pdf_preview['scale'] * -scale
                else:
                    self.pdf_preview['scale'] = scale
            pdf_preview.set_size_request(int(self.pdf_preview['width']*scale), int(self.pdf_preview['height']*scale))
            self.ui.get_widget('button_zoom_out').set_sensitive( scale>0.3 )
            self.ui.get_widget('button_zoom_in').set_sensitive( True )
            self.ui.get_widget('button_zoom_normal').set_sensitive( True )
            self.ui.get_widget('button_zoom_best_fit').set_sensitive( True )
            if redraw: pdf_preview.queue_draw()
            return scale
        else:
            pass
        
    def on_expose_pdf_preview(self, widget, event):
        if not self.pdf_preview.get('current_page'): return
        cr = widget.window.cairo_create()
        cr.set_source_rgb(1, 1, 1)
        scale = self.pdf_preview['scale']
        if scale==None:
            scale = (self.ui.get_widget('pdf_preview').get_parent().get_allocation().width-2.0) / self.pdf_preview['width']
        if scale != 1:
            cr.scale(scale, scale)
        cr.rectangle(0, 0, self.pdf_preview['width'], self.pdf_preview['height'])
        cr.fill()
        self.pdf_preview['current_page'].render(cr)


    def refresh_preview(self):
        if os.path.isfile( self.pdf_file ): os.remove( self.pdf_file )

        text_buffer = self.editor.get_buffer()
        tex = text_buffer.get_text( text_buffer.get_start_iter(), text_buffer.get_end_iter() )
        ftex = open( self.tex_file, 'w' )
        ftex.write( tex )
        ftex.close()
        
        os.chdir('/tmp')
        child_stdin, child_stdout = os.popen2( 'pdflatex -file-line-error-style -src-specials -halt-on-error "%s"' % self.tex_file )
        child_stdin.close()
        output = child_stdout.read()
        child_stdout.close()
        os.chdir(CURRENT_DIR)
        self.ui.get_widget('textview_output').get_buffer().set_text(output)
        
        self.refresh_pdf_preview_pane()
        self.changed_time = None
        
    def exit(self):
        if os.path.isfile( self.tex_file ): os.remove( self.tex_file )
        if os.path.isfile( self.pdf_file ): os.remove( self.pdf_file )
        sys.exit(0)
        

    def new(self):
        text_buffer = self.editor.get_buffer()
        self.current_file = None
        text_buffer.set_text('')
        self.ui.get_widget('menu_save').set_sensitive( self.current_file!=None )
        self.ui.get_widget('toolbutton_save').set_sensitive( self.current_file!=None )


    def open(self):
        global CURRENT_DIR
        os.chdir(CURRENT_DIR)
        dialog = gtk.FileChooserDialog(title='Select a TEX file...', parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK), backend=None)
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            CURRENT_DIR = dialog.get_current_folder()
            filename = dialog.get_filename()
            self.open_file( filename )
        dialog.destroy()
        
    
    def open_file(self, filename):
        if not os.path.isfile(filename):
            self.new()
            return
        text_buffer = self.editor.get_buffer()
        self.current_file = filename
        f = open( self.current_file )
        text_buffer.set_text( f.read() )
        f.close()
        self.ui.get_widget('menu_save').set_sensitive( self.current_file!=None )
        self.ui.get_widget('toolbutton_save').set_sensitive( self.current_file!=None )
        self.refresh_preview()
        self.changed = False
        self.main_window.set_title( PROGRAM +' - '+ self.current_file )
        self.retag( text_buffer, text_buffer.get_start_iter(), text_buffer.get_end_iter() )
        


    def save_as(self):
        global CURRENT_DIR
        os.chdir(CURRENT_DIR)
        dialog = gtk.FileChooserDialog(title='Save TEX file...', parent=None, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK), backend=None)
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            CURRENT_DIR = dialog.get_current_folder()
            self.current_file = dialog.get_filename()
            self.save()
        dialog.destroy()
        
    
    def save(self):
        text_buffer = self.editor.get_buffer()
        tex = text_buffer.get_text( text_buffer.get_start_iter(), text_buffer.get_end_iter() )
        ftex = open( self.current_file, 'w' )
        ftex.write( tex )
        ftex.close()
        self.changed = False
        self.main_window.set_title( PROGRAM +' - '+ self.current_file )
        
    
    def save_pdf(self):
        o_filename = self.current_file
        if o_filename.endswith('.tex'):
            o_filename = o_filename[:-4]
        o_filename = o_filename +'.pdf'
        
        child_stdin, child_stdout = os.popen2( 'cp "%s" "%s"' % (self.pdf_file, o_filename) )
        child_stdin.close()
        output = child_stdout.read()
        child_stdout.close()
        
    
    def watch_editor(self):
        while True:
            if self.changed_time: # and (datetime.now() - self.changed_time).seconds > 2:
                text_buffer = self.editor.get_buffer()
                self.retag( text_buffer, text_buffer.get_start_iter(), text_buffer.get_end_iter() )
                self.refresh_preview()
            time.sleep(1)


if __name__ == "__main__":
    
    global main_gui
    main_gui = MainGUI()
    
    if sys.argv[1] and os.path.isfile( sys.argv[1] ):
        main_gui.open_file(sys.argv[1])
    
    gtk.main()



