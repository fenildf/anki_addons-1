# -*- coding: utf-8 -*-

import sys
import collections
from aqt.main import AnkiQt
from anki.hooks import wrap
from PyQt4.QtGui import *
from aqt import mw


def _keyPressEvent(self, evt, _old):
    key = str(evt.text())
    if key == "v":
        onVoid(self, "")
    _old(self, evt)


def onVoid(self, search=""):
    void_prompt_window_create()


AnkiQt.onCram = wrap(AnkiQt.onCram, onVoid, "around")
AnkiQt.keyPressEvent = wrap(AnkiQt.keyPressEvent, _keyPressEvent, "around")


# added function to handle on button press
def void_prompt_window_create():
    # create window
    mw.void_prompt = QDialog(mw)
    mw.void_prompt.setWindowTitle("Create Void Deck")
    mw.void_prompt.setMinimumWidth(400)
    mw.void_prompt.setMinimumHeight(90)

    # create deck_name widget
    deck_name_label = QLabel("query:", mw.void_prompt)
    deck_name_text  = QLineEdit()

    # create combo box
    if 'savedFilters' in mw.col.conf.keys() and len(mw.col.conf['savedFilters']) > 0:
        search_combo_box_label = QLabel(_("saved search: "))
        search_combo_box_items = QComboBox()
        search_combo_box_items.addItem("", "")

        search_items = collections.OrderedDict(sorted(mw.col.conf['savedFilters'].items()))
        for key, value in search_items.items():
            search_combo_box_items.addItem(key, value)

    # create dialog button
    dialog_button_box   = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    dialog_button_box.button(QDialogButtonBox.Ok).clicked.connect(void_filter_deck_create)
    dialog_button_box.button(QDialogButtonBox.Cancel).clicked.connect(mw.void_prompt.close)

    # set layout
    layout = QGridLayout(mw.void_prompt)
    layout.addWidget(deck_name_label, 0, 0)
    layout.addWidget(deck_name_text, 0, 1)

    if 'savedFilters' in mw.col.conf.keys() and len(mw.col.conf['savedFilters']) > 0:
        layout.addWidget(search_combo_box_label, 1, 0)
        layout.addWidget(search_combo_box_items, 1, 1)

    layout.addWidget(dialog_button_box, 2, 1)
    layout.activate()
    mw.void_prompt.resize(layout.sizeHint())

    # set default focus
    deck_name_text.setFocus()

    # bind shortcuts
    QShortcut(QKeySequence("Esc"),   mw.void_prompt, mw.void_prompt.close)

    # show window
    mw.void_prompt.show()


def void_filter_deck_create(self):
    import aqt.dyndeckconf

    # get name of deck or potentially search string
    deck_name_text = mw.void_prompt.findChildren(QLineEdit)[0].text()

    # early return in case of completely empty input
    if deck_name_text == "" and len(mw.void_prompt.findChildren(QComboBox)) <= 0:
        mw.moveToState("deckBrowser")
        mw.void_prompt.close()
        return

    # set deck_name_text to placeholder 'void' if it is empty
    if deck_name_text == "":
        deck_name_text = "void"

    # retrieve the saved search query
    search_query = ""
    if 'savedFilters' in mw.col.conf.keys() and len(mw.col.conf['savedFilters']) > 0:
        selectedComboItem = mw.void_prompt.findChildren(QComboBox)[0]
        search_query = selectedComboItem.itemData(selectedComboItem.currentIndex())

    # set search information to look for a deckname
    search = ""
    deck = mw.col.decks.current()

    # create new dynamic deck
    deck_name_text_tags = deck_name_text.split(' ')
    if ":" in deck_name_text_tags[0]:
        did = mw.col.decks.newDyn(deck_name_text)
    else:
        did = mw.col.decks.newDyn(deck_name_text_tags[0])

    if ":" in deck_name_text:
        if ":" in deck_name_text_tags[0]:
            search += deck_name_text + ' '
        else:
            for s in deck_name_text_tags[1:]:
                search += s + " "
    elif not search_query:
        if not deck['dyn']:
            search = 'deck:"%s" ' % deck['name']

    if search_query != "" or search != "":
        search += search_query
        diag = aqt.dyndeckconf.DeckConf(mw, first=True, search=search)
        if not diag.ok:
            # user cancelled first config
            mw.col.decks.rem(did)
            mw.col.decks.select(deck['id'])
        else:
            mw.moveToState("deckBrowser")
    else:
        mw.col.decks.rem(did)
        mw.moveToState("deckBrowser")
    mw.void_prompt.close()

