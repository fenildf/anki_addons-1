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

def splitShuffle(expr, t):
    expr = stripHTML(expr).strip()
    if t == SGJ:       
        from rakutenma import RakutenMA    
        rma = RakutenMA(phi=1024, c=0.007812)
        tD, tF = os.path.split(__file__)
        jSon = os.path.join(tD, 'model_ja.min.json')     
        rma.load(jSon)           
        resultl = rma.tokenize(expr)  
        result = [r for r, s in resultl]
    elif t in SGC:    
        import jieba
        result = jieba.cut(expr, cut_all=False)  
    elif t == JSS:    
        result = expr.split(' ')
    elif t in WRAPL:
        result = list(expr)
    newResult, glosses = getResult(result, t)
    jn = u''
    full = jn.join(newResult)
    random.shuffle(newResult)     
    strResult = u''.join(newResult)     
    return strResult, full, glosses
   
def sentGloss(res, t):
    """
        Fall back to reading-based Japanese lookup
        if headword lookup fails. Chinese lookup
        multi-pronged by default.
        """               
    if t == SGJ:
        from cjklib.dictionary import EDICT    
        d = EDICT()
        dtrans = d.getForHeadword(res)    
    elif t == SGC or t == SGCW: 
        from cjklib.dictionary import CEDICT
        d = CEDICT()
        if res in cedict.all:
            dtrans = d.getFor(res)
        else: return ''
    entries = [] 
    entry = ''
    for e in dtrans:
        for f in e._fields:
            if getattr(e, f) != None:
                entry = unicode(getattr(e, f)) + u'\t'
                entries.append(entry)
    if len(entries) == 0:
        for e in d.getForReading(res):
            for f in e._fields:
                if getattr(e, f) != None:
                    entry = unicode(getattr(e, f)) + u'\t'
                    entries.append(entry)
    return u'\t'.join(entries)
        
def getResult(result, t):
    """
        Use random to ensure 
        uniqueness of IDs, just in
        case.
        """
    glosses = []
    random.seed(2)
    count = random.random()
    newResult = []
    blacklist = [u' ', u'　', u'\xa0', u'？', u'！', u'。', u'、', u'.', u'!', u'?', u',']  
    if 'Chinese' in t: l = 'zh'
    elif 'Japanese' in t: l = 'ja'
    else: l = 'sp'
    for res in result:
        trans = ''
        if res not in blacklist:
            if t == JSS or t == JSW:
                for p in blacklist: res = res.replace(p, "")
            count += 1.0
            id = '%sUnshuffle' % (l) + str(count)
            if t != JSS and t != JSW:
                if t in WRAPL:
                        from kanRen import glossKanji
                        resk = u''.join(re.findall('[%s]' % hanzi.characters, res, re.UNICODE))
                        if resk:
                            if t == SGCW and resk in cedict.all:
                                trans = sentGloss(resk, t)
                            elif t != SGCW: trans = glossKanji(resk, t)
                else: 
                    trans = sentGloss(res, t)
                if trans: glosses.append(u'• ' + trans)
            newResult.append('''<div class="copyt" onclick="copyrem( document.getElementById('%s').innerText, document.getElementById('%s') );" id="%s" style="padding: 1px; margin: 2px; box-shadow: 0px 0px 0px 1px rgba(0,0,0,0.3); cursor: pointer; border-radius: 5px; display: inline-block;" title="%s">%s</div>''' % (id, id, id, trans, res))    
    glosses = u'<br>'.join(glosses)
    return newResult, glosses