# -*- coding: utf-8 -*-
# Copyright: Luminous Spice <luminous.spice@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# This simple Add-on automatically adds a tag on your mature notes after the review.
# GitHub: https://github.com/luminousspice/anki-addons/

#1) This is a simple modification of the above add-on to tag a card and fill a field 'Learned'
#   (if you have such a field), which represents knowing a card well enough to switch templates,
#   reverse it, study the content elsewhere, etc.
#   By default the setting is 7 but I think anywhere under two weeks should work well.
#   You can use 'selective card generation' (see Anki manual) to automatically create
#   new cards of a certain template style when the field is filled.

#2) Will suspend cards once they reach a certain interval/pass count if they have the opt-in tag[s]--
#   the tag[s] will be removed after suspension; a tooltip will notify you of the suspension.

#3) Removes a tag of your choosing when the tag removal threshold is met,
#   so you can classify and prioritize cards by urgency until they're well-learned.

from anki.hooks import wrap
from anki.sched import Scheduler
from aqt import mw
from aqt.utils import tooltip

# Threshold learned interval
# According to researchers, one week interval good for a semester (1-3 months).
threshold = 7 # Learned well enough interval >= this many days.
threshold_reps = 5 # Learned well enough after this many passes.
# Tag string for learned note
LearnedTag = u"Learned"
LearnedTag_reps = u"Learned_reps"

#Opt-in tags for auto-suspension
optTag = u"suspendable" # cards with this tag will be auto-suspended by interval
optTag_reps = u"suspendable_reps" # cards with this tag will be auto-suspended by # passes

# Threshold suspend interval
suspendThreshold = 40 # suspend @ interval >= this many days
# Researchers recommend 3-4 spaced sessions total (one pass per session).
suspendThreshold_reps = 5 # suspend @ this many passes [reps - lapses]

#Remove tag threshold
removeThreshold = 7 # Remove tag when interval >= this many days. 7 days good for exams.
removeThreshold_reps = 2 # Remove specified tag when passes >= this number.
removeTag = u"urgent" # Removed by interval size.
removeTag_reps = u"urgent_reps" # Removed by pass count.

def susp_learn_rem_check(self, card, ease):
    f = card.note()
    passes = card.reps - card.lapses
    if (card.ivl >= threshold):
        # @ivl>= x days, add 'Learned' tag, fill Learned field
        f.addTag(LearnedTag)
        if 'Learned' in mw.col.models.fieldNames(f.model()):
            if not f['Learned']:
                f['Learned'] = 'Yes'
    if (passes >= threshold_reps):
        # @ >= a passes, add 'Learned_reps' tag, fill Learned_reps field
        f.addTag(LearnedTag_reps)
        if 'Learned_reps' in mw.col.models.fieldNames(f.model()):
            if not f['Learned_reps']:
                f['Learned_reps'] = 'Yes'
    if (card.ivl >= suspendThreshold):
        # @ivl>= y days, suspend card, remove opt-in tag
        if f.hasTag(optTag): # Opt-in: no suspension if no 'suspendable' tag.
            if card.queue != -1:
                mw.col.sched.suspendCards([card.id])
                tooltip(_(
                    "Card suspended, reached interval of %s days." % suspendThreshold))
                f.delTag(optTag)
    if (passes >= suspendThreshold_reps):
        # @ >= b passes, suspend card, remove opt-in tag
        if f.hasTag(optTag_reps): # Opt-in: no suspension if no 'suspendable_reps' tag.
            if card.queue != -1:
                mw.col.sched.suspendCards([card.id])
                tooltip(_(
                    "Card suspended, reached %s passes." % suspendThreshold_reps))
                f.delTag(optTag_reps)
    if (card.ivl >= removeThreshold):
        # @ivl>= z days, remove 'urgent' tag.
        if f.hasTag(removeTag):
            f.delTag(removeTag)
    if (passes >= removeThreshold_reps):
        # @ >= c passes, remove 'urgent_reps' tag.
        if f.hasTag(removeTag_reps):
            f.delTag(removeTag_reps)
    f.flush()
    return True

Scheduler.answerCard = wrap(Scheduler.answerCard, susp_learn_rem_check)
