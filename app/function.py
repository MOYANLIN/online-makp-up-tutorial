def addtwodimdict(thedict, key_a, key_b, val):   #implementation of 2D dict
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})
