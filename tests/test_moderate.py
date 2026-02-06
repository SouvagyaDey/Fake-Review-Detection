import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.inference import moderation_action

def test_spam_block():
    assert moderation_action("spam", 0.95) == "BLOCK"

def test_spam_manual_review():
    assert moderation_action("spam", 0.6) == "MANUAL_REVIEW"

def test_spam_approve():
    assert moderation_action("spam", 0.3) == "APPROVE"

def test_not_spam_always_approve():
    assert moderation_action("not_spam", 0.99) == "APPROVE"
