__author__ = 'JAPeTo <jeffersonamado@gmial.com>'
import os
import sys

def alg_first_fit(data=None):
    _blocks = data['mem']
    _jobs = data['jobs']
    assignation = {id:[] for id in _blocks}
    for proc in _jobs:
        for b_id in _blocks:
            b_size = _blocks[b_id]
            if b_size >= proc['size']:
                _blocks[b_id] =  _blocks[b_id] - proc['size']
                assignation[b_id].append( proc['name'] )
                break
    data['assignation'] = assignation
    return data
