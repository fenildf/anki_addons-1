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
from kdsgSAC import *

def glossKanji(k, t):
    from cjktools.resources import kanjidic
    kjd = kanjidic.Kanjidic()
    try: entry = kjd[k]
    except: return ''
    kanji = u' '.join(entry.kanji)    
    gloss = '[' + u', '.join(entry.gloss) + ']'
    on_r = '[' + u', '.join(entry.on_readings) + ']'
    kun_r = '[' + u', '.join(entry.kun_readings[:4]) + ']'
    if t == KDSG or t == GLOSS: 
        return u'%s %s %s' % (gloss, on_r, kun_r)        
    elif t == KSG: 
        return u'• %s: %s %s %s' % (kanji, gloss, on_r, kun_r)
    elif t in WRAPL:
        return u'%s: %s %s %s' % (kanji, gloss, on_r, kun_r)      
    
def decompKanji(ch):
    """
        Replace placeholders in results
        with proper subcomponents.
        Make sure kanji itself not in results;
        fall back on stroke order decomposition
        where available.
        """
    from cjktools.resources.radkdict import RadkDict        
    radk = RadkDict()
    rd = {u'\u5E76': u'\u4E37', u'\u6EF4': u'\u5547', u'\u5316': u'\u2E85', 
    u'\u827E': u'\u2EBE', u'\u5208': u'\u2E89', u'\u8FBC': u'\u2ECC', 
    u'\u521D': u'\u8864', u'\u5C1A': u'\u2E8C', u'\u8CB7': u'\u7F52', 
    u'\u72AF': u'\u72AD', u'\u5FD9': u'\u5FC4', u'\u793C': u'\u793B', 
    u'\u4E2A': u'\uD840\uDDA2', u'\u8001': u'\u2EB9', u'\u624E': u'\u624C', 
    u'\u6770': u'\u706C', u'\u7594': u'\u7592', u'\u79B9': u'\u79B8', 
    u'\u90A6': u'\u2ECF', u'\u9621': u'\u2ED6', u'\u6C41': u'\u6C35'}
    try: ls = radk[ch]
    except: return auxSOrd(ch)
    ls = [rd[i] if i in rd else i for i in ls]  
    ls = [i if i != ch else auxSOrd(i) for i in ls]
    random.shuffle(ls)
    decomp = u' '.join([i for i in ls if i])
    return decomp      
    
def procK(x, kl, t):        
    fin = [(glossKanji(k, t)) for k in kl if (glossKanji(k, t))]             
    if t == KDSG:
        dkl = [u'• ' + decompKanji(k) + ': ' for k in kl if decompKanji(k)]
        fin = [i + j for i, j in zip(dkl, fin)]
    else:
        if t == GLOSS:
            fin = [u'• ' + fk for fk in fin if fk]  
        elif t == DECOMP:
            fin = [(u'• ' + decompKanji(k)) for k in kl if decompKanji(k)]                
    random.shuffle(fin)
    return fin    

def jumble(x, kl):
    jun = ''
    kll = re.findall('[%s]' % hanzi.characters, x, re.UNICODE)
    for i in x:
       if i in kl:
           j = random.choice(kll)
           jun += j
           kll.remove(j)
       else: jun += i  
    return jun    

def getStrokeOrd(fin, kl):
    """
        Trying for awareness of glyph locale
        in lookup.
        """    
    from cjklib.characterlookup import CharacterLookup        
    for i in kl:
        if i in cedict.simplified: cjk = CharacterLookup('C')
        elif i in cedict.traditional: cjk = CharacterLookup('T')                
        else: cjk = CharacterLookup('J')
        j = cjk.getStrokeOrder(i)
        fin.append(u'• ' + u' '.join(j)) 
    return fin    

def auxSOrd(i):
    """
        Try to get stroke decomposition
        if subcomponent decomposition fails.
        """
    from cjklib.characterlookup import CharacterLookup        
    if i in cedict.simplified: cjk = CharacterLookup('C')
    elif i in cedict.traditional: cjk = CharacterLookup('T')                
    else: cjk = CharacterLookup('J')
    try: j = cjk.getStrokeOrder(i)    
    except: return u'[x]'
    return u' '.join(j)