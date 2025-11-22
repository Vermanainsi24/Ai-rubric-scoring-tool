import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)

FILLER_WORDS = set([
    "um", "uh", "like", "you know", "so", "actually", "basically",
    "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"
])

def normalize_text(text):
    if text is None:
        return ""
    return text.strip()

def tokenize(text):
    return word_tokenize(text)

def word_count(text):
    return len(tokenize(text))

def sentence_count(text):
    return max(1, len(re.split(r'[.!?]+', text)) - 1)
