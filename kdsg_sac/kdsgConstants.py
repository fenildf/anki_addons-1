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
#You can customize these string values to change required field names.
#--------------------
SCOLOR = "dimgray"
VERT = 'Vertical'
KDSG = 'KDSG'
KSG = 'KSG'
DECOMP = 'Kanji Decomposition'
GLOSS = 'Kanji Gloss'
JUMBLE = 'Kanji Jumble'
HIRA = 'Roma2Hira'
KATA = 'Roma2Kata'
ZHU = 'Pinyin2Zhuyin'
STROKE = 'Stroke Order'
HANTRAN = 'Hangul2Roma'
TRANHAN = 'Roma2Hangul'
JAMO = 'Jamo Decomposition'
SPACEJ = 'Space_ja'
SPACEC = 'Space_zh'
POSJ = 'PoS_ja'
POSC = 'PoS_zh'
LDJ = 'Lexical_Density_ja'
LDC = 'Lexical_Density_zh'
SGJ = 'Shuffle and Gloss Japanese Sentence'
SGJF1 = 'ShuffledSent_ja'
SGJF2 = 'AnswerSent_ja'
SGJF3 = 'GlossSent_ja'
SGC = 'Shuffle and Gloss Chinese Sentence'
SGCF1 = 'ShuffledSent_zh'
SGCF2 = 'AnswerSent_zh'
SGCF3 = 'GlossSent_zh'
JSS = 'Shuffle Spaced Sentence'
JSSF1 = 'ShuffledSent_sp'
JSSF2 = 'AnswerSent_sp'
SGJW = 'Shuffle and Gloss Japanese Word'
SGJWF1 = 'ShuffledWord_ja'
SGJWF2 = 'AnswerWord_ja'
SGJWF3 = 'GlossWord_ja'
SGCW = 'Shuffle and Gloss Chinese Word'
SGCWF1 = 'ShuffledWord_zh'
SGCWF2 = 'AnswerWord_zh'
SGCWF3 = 'GlossWord_zh'
JSW = 'Shuffle non-CJ Word'
JSWF1 = 'ShuffledWord_sp'
JSWF2 = 'AnswerWord_sp'
SOURCES = 'Expression'
SOURCEW = 'Word'
#--------------------

#Don't touch.
#--------------------
TARGS = [VERT, KDSG, KSG, DECOMP, GLOSS, 
         JUMBLE, STROKE, HIRA, KATA, 
         JAMO, HANTRAN, TRANHAN, ZHU, SPACEJ, 
         SPACEC, POSJ, POSC, LDJ, LDC] 
TRANSL = [HANTRAN, TRANHAN, ZHU, HIRA, KATA]
TOKJ = [POSJ, LDJ, SPACEJ]
TOKC = [POSC, SPACEC, LDC]
WRAP = [SGJ, SGC, JSS, SGJW, SGCW, JSW]
WRAPL = [SGJW, SGCW, JSW]
BFW = [KDSG, KSG, STROKE, JAMO, DECOMP, GLOSS]
RSGJW = u', '.join([SGJWF1, SGJWF2, SGJWF3])
RSGCW = u', '.join([SGCWF1, SGCWF2, SGCWF3])
RJSW = u', '.join([JSWF1, JSWF2])
RSGJ = u', '.join([SGJF1, SGJF2, SGJF3])
RSGC = u', '.join([SGCF1, SGCF2, SGCF3])
RJSS = u', '.join([JSSF1, JSSF2])
DST = {SGJW: (SOURCEW, RSGJW), SGCW: (SOURCEW, RSGCW), 
JSW: (SOURCEW, RJSW), SGJ: (SOURCES, RSGJ), 
SGC: (SOURCES, RSGC), JSS: (SOURCES, RJSS), 
KDSG: (SOURCEW, KDSG), KSG: (SOURCEW, KSG), JAMO: (SOURCEW, JAMO),
STROKE: (SOURCEW, STROKE), DECOMP: (SOURCEW, DECOMP), GLOSS: (SOURCEW, GLOSS)}
HPUNK = [u'。', u'！', u'…', u'、', u'：', u'？', u'；', u'「', u'」', 
        u'《', u'》', u'［', u'］', u'｛', u'｝', u'【', u'】', u'〈', u'〉', 
        u'『', u'』', u'ー', u'～']
VPUNK = [u'︒', u'︕', u'︙', u'︑', u'︓', u'︖', u'︔', u'﹁', u'﹂', 
        u'︽', u'︾', u'﹇', u'﹈', u'︷', u'︸', u'︻', u'︼', u'︿', u'﹀',
        u'﹃', u'﹄', u'∣', u'⌇']
#--------------------