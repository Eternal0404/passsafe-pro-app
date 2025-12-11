import math
import string

def check_strength(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32
    entropy = len(password) * math.log2(pool) if pool else 0
    if entropy < 40:
        return 'weak'
    elif entropy < 60:
        return 'medium'
    else:
        return 'strong'