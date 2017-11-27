# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Title: CJK Scalpel: Stand Alone Complex 
        (No Internet connection or website required.)

Evolved from my many modifications of Kenishi's Anki 2 port of
    overture2112's Sentence Gloss Plugin.

[x] in decomposition results means the part is the same as the 
    character and would give away the answer.

Kanji Decomposition and Glossing via Lars Yencken's cjktools: 
    https://github.com/larsyencken/cjktools/blob/master/LICENSE.txt

Stroke order decomposition via Christoph Burgmer's cjklib: 
    https://pypi.python.org/pypi/ninchanese-cjklib/

Romaji transliteration via romkan, a Python port (by Masato Hagiwara) 
    of a Ruby script written by Satoru Takabayashi: 
    https://pypi.python.org/pypi/romkan/0.2.1

Pinyin transliteration via Dragonmapper: 
    http://dragonmapper.readthedocs.io/en/latest/tutorial.html

Hangul transliteration via Lee Sun-yeon's hangul.translit and Dan Rasband's krtpy: 
    https://pypi.python.org/pypi/hangul.translit/0.1.1 
    https://code.google.com/archive/p/krtpy/

Jamo decomposition via Kang Min Yoo's hangul-utils: 
    https://github.com/kaniblu/hangul-utils/blob/master/LICENSE 

Japanese segmentation and annotation makes use of Masato Hagiwara's Rakuten MA.
   RakutenMA Python port by Yukino Ikegami (https://pypi.python.org/pypi/rakutenma).
   For both versions: Apache License version 2.0
   Rakuten MA Python (c) 2015- Yukino Ikegami. All Rights Reserved.
   Rakuten MA (original) (c) 2014 Rakuten NLP Project. All Rights Reserved.
   
Chinese segmentation and annotation makes use of Sun Junyi's jieba: 
    https://github.com/fxsjy/jieba/blob/master/LICENSE
"""

__version__ = '1.0.6'

from anki.hooks import addHook, wrap
from anki.notes import Note
from anki.utils import stripHTML
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
import random, re, os
from kdsgConstants import *
from zhon import hanzi, cedict, pinyin

def decGlo(expr, t):
    """
        Preprocessing source text
        and routing to and from the 
        appropriate processors.
        """
    fin = []
    x = stripHTML(expr).strip()
    if t in TOKJ or t in TOKC:
        from tokLex import tokenize    
        # PoS, Lexical Density.            
        return tokenize(x, t)  
    if t == JAMO:
        from transL import jamo    
        # Jamo decomposition.
        return jamo(x)
    if t == VERT:
        from transL import tategaki    
        # Convert to vertical text.
        return tategaki(x)        
    if t in TRANSL:
        from transL import trans
        # Transliteration.
        return trans(x, t)
    kl = re.findall('[%s]' % hanzi.characters, x, re.UNICODE)  
    if t == JUMBLE: 
        from kanRen import jumble    
        # Kanji jumble       
        return jumble(x, kl)          
    if t == STROKE: 
        from kanRen import getStrokeOrd
        # Stroke decomposition           
        fin = getStrokeOrd(fin, kl)
    else:
        from kanRen import procK
        # KDSG, kanji gloss, kanji decomposition    
        fin = procK(x, kl, t)
    return u'<br>'.join(fin)
 
def dGlo(f, t): 
    """
        Assign the appropriate sources
        for processing and send results 
        to the appropriate target fields.
        """        
    if t in WRAP:
        # o+1: SAC
        from o1SAC import splitShuffle          
        if t in WRAPL:
            # Words
            s = SOURCEW        
            if t == SGJW:
                if f[SGJWF1]: return
                f[SGJWF1], f[SGJWF2], f[SGJWF3] = splitShuffle(f[s], t)
            if t == SGCW:
                if f[SGCWF1]: return
                f[SGCWF1], f[SGCWF2], f[SGCWF3] = splitShuffle(f[s], t)   
            if t == JSW:
                # No glossing for non-CJ yet.
                if f[JSWF1]: return
                f[JSWF1], f[JSWF2], d = splitShuffle(f[s], t)    
        else:
            # Expressions
            s = SOURCES
            if t == SGJ:
                if f[SGJF1]: return
                f[SGJF1], f[SGJF2], f[SGJF3] = splitShuffle(f[s], t)
            if t == SGC:
                if f[SGCF1]: return            
                f[SGCF1], f[SGCF2], f[SGCF3] = splitShuffle(f[s], t) 
            if t == JSS:
                # No glossing for non-CJ yet.
                if f[JSSF1]: return                
                f[JSSF1], f[JSSF2], d = splitShuffle(f[s], t) 
    else:
        # Standard CJK Scalpel
        if f[t]: return
        if t in BFW: 
            # Words
            f[t] = decGlo(f[SOURCEW], t) 
        else:
            # Expressions
            f[t] = decGlo(f[SOURCES], t)    
    
def setupMenu(ed, m, i, j):
    """Implement genMenu."""
    i = QAction('%s' % j, ed)
    ed.connect(i, SIGNAL('triggered()'), lambda e=ed: 
            onKDSG(e, j))
    m.addAction(i)       
    
def genMenu(ed):  
    """
        Cycle through constants, generating
        variables/actions to setup menus
        as we go.
        """
    ed.form.menuEdit.addSeparator() 
    ed.cjkMenu = QMenu(_('&CJK Scalpel'), ed)
    ed.form.menuEdit.insertMenu(ed.form.menuEdit.menuAction(), ed.cjkMenu)
    ed.form.menuEdit.addSeparator()     
    ed.o1Menu = QMenu(_('&o+1: SAC'), ed)
    ed.cjkMenu.addMenu(ed.o1Menu)
    ed.cjkMenu.addSeparator()         
    for i, j in zip([None] * len(TARGS), TARGS): 
        setupMenu(ed, ed.cjkMenu, i, j) 
    for i, j in zip([None] * len(WRAP), WRAP): 
        setupMenu(ed, ed.o1Menu, i, j)         

def onKDSG(ed, t):
    """
        Initiate actions on notes for selected
        cards in browser.
        """
    n = '%s' % t
    ed.editor.saveNow()
    runKDSG(ed, ed.selectedNotes(), t)   
    mw.requireReset()

def refreshSession(): mw.col.s.flush()

def getST(t):
    """
        Get proper source and target
        field names for error notification.
        """
    if t in DST: return DST[t][0], DST[t][1]
    else: return SOURCES, t
	
def runKDSG(ed, fids, t):
    """
        Cycle through, applying appropriate
        processing, notify of proper source/target
        fields if they cause error, otherwise just
        a generic exception with traceback.
        """
    mw.progress.start(max=len(fids), immediate=True)
    for (i, fid) in enumerate(fids):
        mw.progress.update(label='%s... ' % (t), value=i)    
        f = mw.col.getNote(id=fid)
        try: dGlo(f, t)
        except:
            import traceback
            sorce, targt = getST(t)
            if '_fieldOrd' in traceback.format_exc():
                showInfo(_(
                '''
                                        Check your field names.<br>
                                        Required source field: %s<br>
                                        Required target fields: %s<br>
                                     ''' % (sorce, targt)) )
                break
            traceback.print_exc()
        try: f.flush()
        except: raise Exception()
        ed.onRowChanged(f, f)
    mw.progress.finish()

def getScrip(varsp):
    """
        JS to be placed on front template.
        Toggles between copy/replace functions,
        color for copied can be changed in constants
        file. Prepended line breaks and removed inner
        breaks to make more distinct and
        compact on template at cost of readability.
        """
    scrip = '''

<script>var isSP = ' '; var notSP = ''; function copytext(text) {text %s; var textField = document.getElementById("typeans"); var caretPos = textField.selectionStart; var front = (textField.value).substring(0, caretPos); var back = (textField.value).substring(textField.selectionEnd, textField.value.length); textField.value = front + text + back;} function remtext(text) {text %s; var textField = document.getElementById("typeans"); textField.value =  textField.value.replace(text, "");} function copyrem(text, e) {if (e.className == "copyt") {e.style.background = "%s"; e.className = "rem"; copytext(text);} else {e.className = "copyt"; e.style.background = "inherit"; remtext(text);}}</script>''' % (varsp, varsp, SCOLOR)
    return scrip
    
def addScrip():
    """
        Search for script in
        templates with o+1
        fields; add if not present,
        or toggle between spaced/
        unspaced text input if present, 
        depending on CJ or non-CJ field.
        """
    t = mw.reviewer.card.template()
    if JSSF1 in t['qfmt']:
        varsp = '+= isSP'
        scrip = getScrip(varsp)
        if scrip not in t['qfmt']:
            if 'isSP' in t['qfmt']:
                t['qfmt'] = t['qfmt'].replace('+= notSP', varsp)
            else: t['qfmt'] += scrip        
    elif SGJF1 in t['qfmt'] or SGCF1 in t['qfmt']:
        varsp = '+= notSP'
        scrip = getScrip(varsp)
        if scrip not in t['qfmt']:
            if 'notSP' in t['qfmt']:
                t['qfmt'] = t['qfmt'].replace('+= isSP', varsp)
            else: t['qfmt'] += scrip
        
def _showSACQuestion(self, _old):
    """
        Showing question-side of cards
        triggers the function to ensure
        proper script in template.
        """
    addScrip()
    _old(self)  
  
addHook('browser.setupMenus', genMenu)
    
Reviewer._showQuestion = wrap(
    Reviewer._showQuestion, _showSACQuestion, 'around')    