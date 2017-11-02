#-*- coding: utf-8 -*-
from morphemes import getMorphemes, MorphDb
from morphemizer import getMorphemizerByName
from util import addBrowserNoteSelectionCmd, cfg, cfg1, getFilter, infoMsg, QInputDialog, QFileDialog, QLineEdit
import util

def pre( b ): # :: Browser -> State
    tags, ok = QInputDialog.getText( b, 'Enter tags', 'Tags', QLineEdit.Normal, 'hasMorph' )
    if not ok or not tags: return
    path = QFileDialog.getOpenFileName( caption='Open db', directory=util.dbsPath )
    if not path: return
    db = MorphDb( path )
    return { 'b':b, 'db':db, 'tags':unicode(tags) }

def per( st, n ): # :: State -> Note -> State
    #n.delTag( st['tags'] ) # clear tags if they already exist?

    notecfg = getFilter(n)
    if notecfg is None: return st
    morphemizer = getMorphemizerByName(notecfg['Morphemizer'])
    for field in notecfg['Fields']:
        for m in getMorphemes(morphemizer, n[ field ], n.tags):
            if m in st['db'].db:
                n.addTag(st['tags'])
                break

    n.flush()
    return st

def post( st ): # :: State -> State
    infoMsg( 'Tagged all notes containing morphemes in that db' )
    return st

addBrowserNoteSelectionCmd( 'MorphMan: Mass Tagger', pre, per, post, tooltip='Tag all cards that contain morphemes from db', shortcut=None )
