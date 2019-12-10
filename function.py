from difflib import SequenceMatcher
import pinyin

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

a = "不需要"

b = pinyin.get(a, format = 'numerical')
print(b)


