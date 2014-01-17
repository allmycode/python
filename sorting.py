l = [("village", 13, 0.5), ("montenegro", 143, 0.07), ("abacus", 0, 1)]
print l

l.sort()
print l

l.sort(key=lambda t: t[1])
print l

l.sort(key=lambda t: t[2])
print l
