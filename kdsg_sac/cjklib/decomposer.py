# -*- coding: utf-8 -*-
"""
Title: Hanzi Knife

Adds an option in browser to generate decomposition and stroke order for Chinese characters using cjklib.

Set 'Hanzi' field to contain Chinese characters (ideally hanzi, but works for many but not all [e.g., 氷] kanji), have an empty 'StrokeOrder' and/or 'RandomStrokes' field (no quotes in field name), select some cards, and activate Edit>Generate hanzi decomposition. If you have a RandomStrokes field and want to fill it with a randomized version of the StrokeOrder field, uncomment lines 52-54 (backspace the # symbol).

Based on the Sentence Gloss Plugin:
    Original Author: overture2112
    Ported by: Kenishi

This plugin is provided as is without any additional support.
"""
import subprocess, re, random
import characterlookup


#### Get decomposition data
def decomp( expr ):
        if type( expr ) != unicode: expr = unicode( expr )
        cjk = characterlookup.CharacterLookup( 'T' )
        # Character locale for glyph selection, Simplified (C)hinese,
        # (T)raditional Chinese, (J)apanese, (K)orean, (V)ietnamese.
        u = []
        bl = [u'\uFF0C', u'\uFF01', u'\uFF1F', u'\uFF1B', u'\uFF1A', u'\uFF08', u'\uFF09', u'\uFF3B', u'\uFF3D', u'\u3010', u'\u3011', u'\u3002', u'\uFE12', u'\u300E', u'\u300F', u'\u300C', u'\u300D', u'\uFE41', u'\uFE42', u'\u3001', u'\u2027', u'\u300A', u'\u300B', u'\u3008', u'\u3009', u'\uFE4F', u'\uFF5E', u'\u3000', u'\uFE4F', u' ']
        for i in expr:
            if i not in bl:
                j = cjk.getStrokeOrder( i )
                #random.shuffle(j) #randomize stroke order
                u.append( u' '.join( j ) )
        random.shuffle(u) #randomize character order
        return u'<br> '.join( u )
        
def strokes( expr ):
        if type( expr ) != unicode: expr = unicode( expr )
        cjk = characterlookup.CharacterLookup( 'T' )
        # Character locale for glyph selection, Simplified (C)hinese,
        # (T)raditional Chinese, (J)apanese, (K)orean, (V)ietnamese.
        u = []
        for i in expr:
            j = cjk.getStrokeOrder( i )
            u.append( u' '.join( j ) )
        return u'<br> '.join( u )   

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from anki.notes import Note
from anki.utils import stripHTML
from aqt import mw
from aqt.utils import showText, showInfo

#### Update note with decomposition 
def decompNote( f ):
    #if not f['StrokeOrder']: 
     #   strokeOrder = strokes( f['Hanzi'] )
      #  f[ 'StrokeOrder' ] = strokeOrder
    if not f['StrokeOrder']: 
        if f['Hanzi']: 
            dec = decomp( f['Hanzi'] )
            f[ 'StrokeOrder' ] = dec

def setupMenu( ed ):
	a = QAction( 'Generate hanzi decomposition', ed )
	ed.connect( a, SIGNAL('triggered()'), lambda e=ed: onRegenDecomp( e ) )
	ed.form.menuEdit.addSeparator()
	ed.form.menuEdit.addAction( a )

def onRegenDecomp( ed ):
	n = "Generate hanzi decomposition"
	ed.editor.saveNow()
	regenDecomp(ed, ed.selectedNotes() )   
	mw.requireReset()

def refreshSession():
	mw.col.s.flush()
	
def regenDecomp( ed, fids ):
	mw.progress.start( max=len( fids ) , immediate=True)
	for (i,fid) in enumerate( fids ):
		mw.progress.update( label='Generating decomposition... ', value=i )
		f = mw.col.getNote(id=fid)
		try: decompNote( f )
		except:
			import traceback
			print 'decomp failed: '
			if '_fieldOrd' in traceback.format_exc():
                                showInfo(_('Check your field names.'))
                                break
			#traceback.print_exc()
			if not '_fieldOrd' in traceback.format_exc():
                                #showInfo(_('Character: ' + f['Hanzi']))
                                continue
			#traceback.print_exc()            
		try: f.flush()
		except:
			raise Exception()        
		ed.onRowChanged(f,f)
	mw.progress.finish()
	

addHook( 'browser.setupMenus', setupMenu )
