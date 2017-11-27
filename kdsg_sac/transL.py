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

def tategaki(x):
    """
        Fragile: relies on specific range
        of size settings; indents a square,
        more if necessary to avoid columns with
        just a punctuation mark.
        Limited mapping of common punctuation.
        New versions of Anki CSS (writing-mode) 
        will probably render this obsolete.
        No vertical wave dash available.
        """
    vert_css = '''
        font-size: 30px; line-height: 1; -webkit-writing-mode: horizontal-bt; 
        margin:auto; width: 200px; -webkit-column-gap: 0px; 
        position: relative; height: 300px; -webkit-column-count: 5
        '''
    vertli_css = 'display: inline-block; margin-bottom: 150px;'        
    for i, j in zip(HPUNK, VPUNK): x = re.sub(i, j, x)
    fin = list(x)
    l = len(fin)
    wt = int(l % 10 == 0)
    div = 5
    if l < 10: pad = u'<br>' * 15
    else:
        while l > div: div += 10
        pad = div % l
        pad = u'<br>' * (pad + 9 - wt)
        fin = pad + u'<br>'.join(fin[::-1])
    return (u'<ul class="tategaki" style="%s;"><li class="tategakili" style="%s;">' 
            % ('', '') + fin + u'</li></ul>') # can sub vert_css, vertli_css

def jamo(x):
    from hangul_utils import split_syllables
    expr = re.findall(ur'[\uac00-\ud7a3]', x, re.UNICODE)
    ls = [u'• ' + split_syllables(i) for i in expr]
    random.shuffle(ls)
    return u'<br>'.join(ls)      
    
def trans(x, t):
    from hangul import translit
    import transcriptions   
    import krt
    if t == HANTRAN:
        #expr = re.findall(ur'[^ ㄱ-ㅣ가-힣]+', x, re.UNICODE)
        expr = re.findall(ur'[\uac00-\ud7a3]', x, re.UNICODE)
        #ka = krt.romanize(x, 'utf-8') # Yale Romanization.
        expr = u''.join(expr)
        ka = translit.romanize(expr.encode('utf-8')) # Revised Romanization of Korean.
        return x.replace(expr, ka)
    elif t == TRANHAN:
        ka = krt.hangulize(x, 'utf-8') # Yale Romanization.
        return ka.decode('utf-8')
    elif t == ZHU:
        expr = re.findall(pinyin.syllable, x, re.IGNORECASE)
        expr = ' '.join(expr)
        ka = transcriptions.to_zhuyin(expr)
        return x.replace(expr, ka)
    elif t == HIRA or t == KATA:
        expr = re.findall(r"(?i)\b[a-z]+\b", x)
        ka = [subvert(i, t) for i in expr]
    for i in range(len(ka)):
         x = re.sub(expr[i], ka[i], x) 
    return x     
    
def subvert(expr, t):
    import romkan
    expr = re.sub(u'\u014D|\u00F4', 'ou', expr, re.UNICODE)
    expr = re.sub(u'\u016B', 'uu', expr, re.UNICODE)
    expr = re.sub(u'\u0113', 'ee', expr, re.UNICODE)
    expr = re.sub(u'\u0101', 'aa', expr, re.UNICODE)
    if t == KATA: kana = romkan.to_katakana(expr) 
    else: kana = romkan.to_hiragana(expr)
    return kana       