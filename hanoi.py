def check_one(s):
    for i in range(1,len(s)):
        if s[i-1] >= s[i]: return False
    return True


def check(s1, s2, s3):
    return check_one(s1) and check_one(s2) and check_one(s3)

def print_s(name, s):
    print name + ":",
    for l in s:
        print l,
    
    print

def print_ss(time, s1, s2, s3):
    print time
    print_s("s1", s1)
    print_s("s2", s2)
    print_s("s3", s3)

c = 0
def hanoi(n, s1,s2,s3):
    global c
    if n == 0:
        return
    else:
        hanoi(n-1, s1, s3, s2)
        c+=1;
        x = s1[0]
        s3.insert(0, x)
        s1.remove(x)
        hanoi(n-1, s2, s1, s3)
        if not check(s1, s2, s3):
            print "Error"
        if (c % 20) == 0:
            print_ss("time "  + str(c), s1, s2, s3)


def do_hanoi():

    s1 = [1,2,3,4,5, 7, 8, 9]
    s2 = []
    s3 = []
    
    if not check(s1, s2, s3):
        print_ss("Error:", s1, s2, s3)
        return
    print_ss("Start:", s1, s2, s3)

    hanoi(len(s1), s1, s2, s3)
#    hanoi(3, s1, s2, s3)

    print_ss("End:", s1, s2, s3)

    print c
    
do_hanoi()
