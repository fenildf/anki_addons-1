# -*- coding: utf-8 -*-
''' A simple replaceent of the Blind Anki add-on (https://ankiweb.net/shared/info/3882431624).
The BA add-on removes counts, this add-on also removes the headers for the counts (Due, New) and the 'You studied X cards today' message. Seems required to use a dummy number; in the BA add-on it's 1, here I changed to .5 to make it subjectively less obtrusive.
'''
from aqt import mw
from aqt.qt import *
from aqt.main import AnkiQt
import aqt.main
from anki.hooks import wrap
from aqt.utils import getOnlyText
from aqt.overview import Overview
from aqt.reviewer import Reviewer
from aqt.deckbrowser import DeckBrowser

class VoidOverview(Overview):
	@staticmethod
	def dummy():
		return (.5,0,0)

	def _table(self):
		orig = self.mw.col.sched.counts
		self.mw.col.sched.counts = VoidOverview.dummy
		table = Overview._table(self)
		self.mw.col.sched.counts = orig
		return table

class VoidReviewer(Reviewer):
	def _remaining(self):
		return ''

mw.sharedCSS += '''
tr.deck td:nth-child(2), tr.deck td:nth-child(3) {
	font-size:0;
}
'''
def VoidDeckTree(self, nodes, depth=0):
    if not nodes:
        return ""
    if depth == 0:
        buf = """
<tr><th colspan=5 align=left></th><th class=count></th>
<th class=count></th><th class=count></th></tr>"""
        buf += self._topLevelDragRow()
    else:
        buf = ""
    for node in nodes:
        buf += self._deckRow(node, depth, len(nodes))
    if depth == 0:
        buf += self._topLevelDragRow()
    return buf

def VoidStats(self):
    return " "
            
mw.overview = VoidOverview(mw)
mw.reviewer = VoidReviewer(mw)
DeckBrowser._renderDeckTree = VoidDeckTree
DeckBrowser._renderStats = VoidStats