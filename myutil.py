
from time import time
import hashlib

def mytime():
    return int(time() * 1000)

def tsv(data, fields):
    return "\n".join([
        "\t".join([row[f] for f in fields]) if row != 0 else "0"
        for row in data
    ])

# winner = winner's elo score
# loser = loser's elo score
# p = 0..1 (how sure are we that the winner won?)
# returns two values,
#   these are deltas that should be applied
#   to the elo scores of the winner and loser
def eloDeltas(winner, loser, p):
    Rw = winner
    Rl = loser
    
    Qw = 10**(Rw / 400)
    Ql = 10**(Rl / 400)
    
    Ew = Qw / (Qw + Ql)
    El = Ql / (Qw + Ql)
    
    Sw = 1
    Sl = 0
    
    K = 32 * p
    
    return (K * (Sw - Ew)), (K * (Sl - El))

def sha1(s):
    return hashlib.sha1(s).hexdigest()

