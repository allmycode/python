import urllib2

def uread(url):
    return urllib2.urlopen(url).read()

open_brackets = 0
close_brackets = 0
level = 0

def main():
    yaru = uread("http://ya.ru")
    
    for i in xrange(0, len(yaru)):
        c = yaru[i]
        if c == '<':
            i = on_open(yaru, i)
        if c == '>':
            i = on_close(yaru, i)

    print "Open brackets: " + str(open_brackets)
    print "Close brackets: " + str(close_brackets)

def on_open(yaru, i):
    global open_brackets
    global level
    open_brackets += 1
    start = i
    if start + 1 < len(yaru):
        if yaru[start + 1] != '/':
            level += 1
        else:
            level -= 1
        
        if yaru[start + 1] != '/':
            for i in xrange(start+1, len(yaru)):
                c = yaru[i]
                if c == '>':                
                    print level*' ' + yaru[start+1:i]
                    if yaru[i - 1] == '/':
                        level -= 1
                    return i
    return i

def on_close(yaru, i):
    global close_brackets
    global level
    close_brackets += 1
    if i > 0 and yaru[i - 1] == '/':
        level -= 1
    return i

if __name__ == "__main__":
    main()
