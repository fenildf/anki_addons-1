# -*- mode: Python ; coding: utf-8 -*-
# • Again Hard (Yes No) 2 buttons only
# https://ankiweb.net/shared/info/1996229983
#
# 2 wide buttons only with smiles instead of words and a bigger font on them.
# It means NO YES in any case.
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016 Dmitry Mikheev, http://finpapa.ucoz.net/
#
# -*- mode: Python ; coding: utf-8 -*-
# • Later not now button
# https://ankiweb.net/shared/info/777151722
# https://github.com/ankitest/anki-musthave-addonz-by-ankitest
# -- tested with Anki 2.0.44 under Windows 7 SP1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Copyright (c) 2016-2017 Dmitry Mikheev, http://finpapa.ucoz.net/
# No support. Use it AS IS on your own risk.
"""
 No answer will be given, next card will be shown.
  Card stays on its place in queue,
   you'll see it next time you study the deck.

    Hotkey: Escape shortcut (Esc).

 inspired by More Answer Buttons for New Cards add-on
 https://ankiweb.net/shared/info/468253198
"""
from __future__ import division
from __future__ import unicode_literals
import os

from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import showText
from anki.hooks import wrap, addHook, runHook
import json
from aqt.qt import *
from anki.utils import intTime
from aqt.main import AnkiQt

# Get language class
import anki.lang
lang = anki.lang.getLang()

#Version of my modifications:
__version__ = '1.0.01'

# Anki uses a single digit to track which button has been clicked.
RETEST = 5

# inspired by
#  Answer_Key_Remap.py
#   https://ankiweb.net/shared/info/1446503737
#  Bigger Show Answer Button
#   https://ankiweb.net/shared/info/1867966335
#  Button Colours (Good, Again)
#   https://ankiweb.net/shared/info/2494384865
#  Bigger Show All Answer Buttons
#   https://ankiweb.net/shared/info/2034935033


remap = {2:  [None, 1, 2, 2, 2],    # - nil     Again   Good   Good    Good  -  default 2-buttons: 1 = Again, 2 = Good, 3=None, 4=None
         3:  [None, 1, 2, 2, 2],    # nil     Again   Good   Good    Good - def 3-buttons: 1 = Again, 2 = Good, 3 = Easy, 4=None
         4:  [None, 1, 3, 3, 3]}    # 0=nil/none   Again Good Good Good - def 4-buttons: 1 = Again, 2 = Hard, 3 = Good, 4 = Easy

# -- width in pixels
# --    Show Answer button, triple, double and single answers buttons
BEAMS4 = '99%'
BEAMS3 = '74%'
BEAMS2 = '48%'
BEAMS1 = '24%'

black = '#000'
red = '#c33'
green = '#3c3'

BUTTON_LABEL = ['<b style="color:'+black+';">Incorrect</b>',
                '<b style="color:'+green+';">Correct</b>']

# Replace _answerButtonList method
def answerButtonList(self):
    l = ((
        1, '<style>button span{font-size:x-large;} button small ' +
        '{ color:#999; font-weight:400; padding-left:.35em; ' +
        'font-size: small; }</style><span>' + BUTTON_LABEL[0] + '</span>',
        BEAMS2),)
    cnt = self.mw.col.sched.answerButtons(self.card)
    if cnt == 2 or cnt == 3: #i believe i did this right: we want ease 2 = good if 2 or 3 buttons
	    return l + ((2, '<span>' + BUTTON_LABEL[1] + '</span>', BEAMS2),)
    elif cnt == 4: # b/c we want ease 3 = good in this version
        return l + ((3, '<span>' + BUTTON_LABEL[1] + '</span>', BEAMS2),)
    # the comma at the end is mandatory, a subtle bug occurs without it

def AKR_answerCard(self, ease):
    count = mw.col.sched.answerButtons(mw.reviewer.card)  # Get button count
    try:
        ease = remap[count][ease]
    except (KeyError, IndexError):
        pass
    __oldFunc(self, ease)

__oldFunc = Reviewer._answerCard
Reviewer._answerCard = AKR_answerCard

def answer_card_intercepting(self, actual_ease, _old):
    ease = actual_ease
    if actual_ease == 1 or actual_ease == RETEST:
        self.mw.col.log()
        self.mw.col.markReview(self.card)
        self.card.lapses += 1
        self.card.reps += 1
        self.mw.col.sched._updateStats(
            self.card, 'time', self.card.timeTaken())
        self.card.mod = intTime()
        self.card.usn = mw.col.usn()
        self.card.flushSched()
        self._answeredIds.append(self.card.id)
        self.mw.autosave()
        id = self.card.id
        self.nextCard()
        if self.card.id == id: self.nextCard()
        return True
    else:
        return _old(self, ease)

Reviewer._answerCard = wrap(
    Reviewer._answerCard, answer_card_intercepting, 'around')

def myAnswerButtons(self, _old):
    times = []
    default = self._defaultEase()

    def but(i, label, beam):
        if i == default:
            extra = 'id=defease'
        else:
            extra = ''
        due = self._buttonTime(i)
        return '''
<td align=center style="width:%s;">%s<button %s %s
onclick='py.link("ease%d");'>
%s</button></td>''' % (
            beam, due, extra,
            ((' title=" '+_('Shortcut key: %s') % i)+' "'), i, label)

    buf = '<table cellpading=0 cellspacing=0 width=100%%><tr>'
    for ease, lbl, beams in answerButtonList(self):
        buf += but(ease, lbl, beams)
    buf += '</tr></table>'
    script = """
    <style>table tr td button { width: 100%; } </style>
<script>$(function () { $('#defease').focus(); });</script>"""
    return buf + script


def myShowAnswerButton(self, _old):
    """
    # Bigger Show Answer Button
    For people who do their reps with a mouse.
    Makes the show answer button wide enough
    to cover all 4 of the review buttons.
    """
    self._bottomReady = True
    if not self.typeCorrect:
        self.bottom.web.setFocus()
    middle = '''
<span class=stattxt>%s</span><br>
<button %s id=ansbut style="display:inline-block;width:%s;%s"
 onclick="py.link('ans');">%s</button>
    </script>
''' % (self._remaining(),
        ((' title=" '+_('Shortcut key: %s') % _('Space'))+' "'),
        BEAMS4, 'font-size:x-large;color:'+black, _('Show Answer'))
    # place it in a table so it has the same top margin as the ease buttons
    middle = (
        '<div class=stat2 align=center ' +
        'style="width:%s!important;">%s</div>') % (BEAMS4, middle)
    if self.card.shouldShowTimer():
        maxTime = self.card.timeLimit() / 1000
    else:
        maxTime = 0
    self.bottom.web.eval('showQuestion(%s,%d);' % (
        json.dumps(middle), maxTime))
    return True

def _keyHandler(self, evt, _old):
    key = str(evt.text())
    if evt.key() == Qt.Key_Escape:
        if self.state == "answer":
            mw.reviewer.nextCard()
    _old(self, evt)

'''
def _keyHandler(self, evt, _old):
    key = str(evt.text())
    if evt.key() == Qt.Key_Escape:
        if self.state == "answer":
            mw.col.log()
            mw.col.markReview(
                mw.reviewer.card)
            mw.reviewer.card.lapses += 1
            mw.reviewer.card.reps += 1
            mw.col.sched._updateStats(
                mw.reviewer.card, 'time',
                mw.reviewer.card.timeTaken())
            mw.reviewer.card.mod = intTime()
            mw.reviewer.card.usn = mw.col.usn()
            mw.reviewer.card.flushSched()
            mw.reviewer._answeredIds.append(
                mw.reviewer.card.id)
            mw.autosave()
            id = mw.reviewer.card.id
            mw.reviewer.nextCard()
            if mw.reviewer.card.id == id:
                mw.reviewer.nextCard()
    _old(self, evt)'''

Reviewer._answerButtons =\
    wrap(Reviewer._answerButtons, myAnswerButtons, 'around')
Reviewer._showAnswerButton =\
    wrap(Reviewer._showAnswerButton, myShowAnswerButton, 'around')
Reviewer._keyHandler = wrap(Reviewer._keyHandler, _keyHandler, "around")
