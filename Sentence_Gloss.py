"""
Title: Sentence Gloss
Tags: gloss, lookup, sentence, japanese, glossing, glosses, jmr, overture2112, wwwjdic, jdic, kenishi

Adds an option in browser to generate glossings for Japanese sentences by polling WWWJDIC. 

Set 'Expression' field to your sentences, have an empty 'Gloss' field, select some cards, and activate Edit>Regenerate Glosses. 

Originally Author: overture2112
Ported by: Kenishi

This plugin is provided as is without any additional support.
"""
# -*- coding: utf-8 -*-
import subprocess, re, urllib, urllib2
from random import shuffle

#### Get gloss data
def url( term ): return 'http://nihongo.monash.edu/cgi-bin/wwwjdic?9ZIH%s' % urllib.quote( term.encode('utf-8') )
def fetchGloss( term ): return urllib.urlopen( url( term ) ).read()
def gloss( expr ):
	if type( expr ) != unicode: expr = unicode( expr )
	print 'glossing:',expr
	x = fetchGloss( expr )
	u = unicode( x, 'utf-8', errors='ignore' )
	ls = re.findall('<li>(.*?)</li>', u )
	return u'<br/>\n'.join( ls )
    
def glossShuffle( expr ):
	if type( expr ) != unicode: expr = unicode( expr )
	print 'glossing:',expr
	x = fetchGloss( expr )
	u = unicode( x, 'utf-8', errors='ignore' )
	ls = re.findall('<li>(.*?)</li>', u )
	shuffle( ls )
	return u'<br/>\n'.join( ls )

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from anki.notes import Note
from anki.utils import stripHTML
from aqt import mw
from aqt.utils import showText

#### Update note with gloss 
def glossNote( f ):
   if f[ 'Gloss' ]: return
   f[ 'Gloss' ] = gloss( f['Expression'] )

def glossShuffleNote( f ):
   if f[ 'Gloss' ]: return
   f[ 'Gloss' ] = glossShuffle( f['Expression'] )
   
def setupMenu( ed ):
	a = QAction( 'Regenerate Glosses', ed )
	b = QAction( 'Regenerate Shuffled Glosses', ed )
	ed.connect( a, SIGNAL('triggered()'), lambda e=ed: onRegenGlosses( e ) )
	ed.connect( b, SIGNAL('triggered()'), lambda e=ed: onRegenShuffledGlosses( e ) )
	ed.form.menuEdit.addSeparator()
	ed.form.menuEdit.addAction( a )
	ed.form.menuEdit.addAction( b )

def onRegenGlosses( ed ):
	n = "Regenerate Glosses"
	ed.editor.saveNow()
	regenGlosses(ed, ed.selectedNotes() )   
	mw.requireReset()

def onRegenShuffledGlosses( ed ):
	n = "Regenerate Glosses"
	ed.editor.saveNow()
	regenShuffledGlosses(ed, ed.selectedNotes() )   
	mw.requireReset()
    
def refreshSession():
	mw.col.s.flush()
	
def regenGlosses( ed, fids ):
	mw.progress.start( max=len( fids ) , immediate=True)
	for (i,fid) in enumerate( fids ):
		mw.progress.update( label='Generating glosses...', value=i )
		f = mw.col.getNote(id=fid)
		try: glossNote( f )
		except:
			import traceback
			print 'gloss failed:'
			traceback.print_exc()
		try: f.flush()
		except:
			raise Exception()
		ed.onRowChanged(f,f)
	mw.progress.finish()
    
def regenShuffledGlosses( ed, fids ):
	mw.progress.start( max=len( fids ) , immediate=True)
	for (i,fid) in enumerate( fids ):
		mw.progress.update( label='Generating glosses...', value=i )
		f = mw.col.getNote(id=fid)
		try: glossShuffleNote( f )
		except:
			import traceback
			print 'gloss failed:'
			traceback.print_exc()
		try: f.flush()
		except:
			raise Exception()
		ed.onRowChanged(f,f)
	mw.progress.finish()
	

addHook( 'browser.setupMenus', setupMenu )
