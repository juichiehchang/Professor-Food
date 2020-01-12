from difflib import SequenceMatcher
import pinyin

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


