ar = ['a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5']
ar2 = ['a1', 'a2', 'b1', 'b2']

def sf(ar, i):
    if len(ar) == 2:
        return
    elif len(ar) == 4:
        a1 = ar[0]
        a2 = ar[1]
        b1 = ar[2]
        b2 = ar[3]
        ar[0] = b1
        ar[1] = a1
        ar[2] = b2
        ar[3] = a2
        return
    else:
        print "+ " + str(ar) 
        t1 = ar[-1]
        t2 = ar[-2]
        ar[-2] = ar[len(ar)/2-1]
        ar[len(ar)/2-1] = t2
        ar[-1] = t1
        t = ar[-1]
        ar[-1] = ar[-2]
        ar[-2] = t
        aa = ar[:-2]
        
        t = aa[len(aa)/2]
        aa[len(aa)/2] = aa[-1]
        aa[-1] = t
        ar[:-2] = aa
        print "- " + str(ar) + " || " + str(aa)
        sf(ar[:-2], i + 1)

sf(ar, 0)
print(ar)
