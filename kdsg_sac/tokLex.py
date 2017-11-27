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

def tokenize(x, t):    
    if t in TOKC:
        from jieba import posseg
        toks = posseg.cut(x)
        if t == POSC:
            return u'\u3000'.join([('%s [%s]' % (f.word, f.flag)) for f in toks])
        elif t == SPACEC:
            return u'\u3000'.join([('%s' % (f.word)) for f in toks])
        else: return lexDens(toks, t)
    elif t in TOKJ:
        from rakutenma import RakutenMA
        rma = RakutenMA()
        rma = RakutenMA(phi=1024, c=0.007812)
        tD, tF = os.path.split(__file__)
        jSon = os.path.join(tD, 'model_ja.min.json') 
        rma.load(jSon)
        toks = rma.tokenize(x)
        if t == SPACEJ: 
            return u'\u3000'.join([i[0] for i in toks])
        elif t == POSJ: 
            return u'\u3000'.join([('%s [%s]' % (i[0], i[1])) for i in toks])
        else: return lexDens(toks, t)
        
def lexDens(toks, t):
    """
        Calculation based on selection of
        tags that various papers suggest should represent
        content words and function words in Japanese and Chinese.
        Therefore approximate.
        """
    content_tags = {'A-c', 'A-dp', 'F', 'J-c', 'J-tari', 'J-xs', 
                 'N-n', 'N-nc', 'N-pn', 'N-xs', 'R', 'V-c', 'V-dp', 
                 'Ag', 'a', 'ad', 'an', 'Dg', 'd', 'i', 'l', 'Ng', 'c', 'nr', 'ns', 'nt', 
                 'nz', 'o', 's', 't', 'Vg', 'v', 'vd', 'vn', 'z', }
    exclude_tags = {'M-aa', 'M-c', 'M-cp', 'M-op', 'M-p', 'S-c', 
                 'S-l', 'U', 'W', 'E', 'w', 'x'}
    content, exclude = 0.0, 0.0
    if t == LDJ:
        for i in toks:
            if i[1] in content_tags: content += 1
            elif i[1] in exclude_tags: exclude += 1
        leng = len(toks)
    if t == LDC:
        leng = 0
        for t in toks:
            leng += 1
            if t.flag in content_tags: content += 1
            elif t.flag in exclude_tags: exclude += 1 
    lexicalDensity = (content / (leng-exclude)) * 100.0    
    return ('%.1f' % lexicalDensity + '%')  