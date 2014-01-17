import StringIO
import re
from sys import argv, stdout

input = open(argv[1] if len(argv) > 1 else 'lorem.txt').read()
output = open(argv[2], 'w') if len(argv) > 2 and argv[2] != '-' else stdout
columns = int(argv[3]) if len(argv) > 3 else 80

def format(acc, out, red=None, N=columns):
    chars = reduce(lambda chars, w: chars + len(w), acc, 0) + (4 if red else 0)
    total_spaces = len(acc)-1
    delta = max(0, N - chars - total_spaces)
    if total_spaces > 0:
        all = delta / total_spaces
        right = delta % total_spaces
    else:
        all = -1
        right = 0

    if red: out.write('    ')

    if chars + total_spaces < N/2:
        out.write(" ".join(acc))
        out.write("\n")
        return

    spaces = total_spaces
    for i in xrange(0, len(acc)):
        out.write(acc[i])
        if spaces != 0:
            out.write(' '*(all+1))
            if spaces <= right: out.write(' ')
            spaces -= 1
    out.write('\n')
    return out

#input = open('lorem.txt').read()
#output = open('res.txt', 'w')

def process_paragraph(p, N=columns):
#    print "Processing: ", p
    acc = list()
    chars = 4
    red = True
    for w in p.split():
        if len(w) + chars + 1 > N:
            format(acc, output, red)
            if red: red = None
            acc = list()
            chars = 0
        acc.append(w)
        chars += len(w) + 1
    format(acc, output, red)


start = 0
lastpos = -1;
last = None
for i, c in enumerate(input):
    if c == '.':
        last = 'd'
        lastpos = i 
    elif c == '\n':
        if last == 'd':
            process_paragraph(input[start:lastpos+1])
            start = i
        elif last == 'n':
            process_paragraph(input[start:lastpos])
            if i - lastpos > 1: 
                process_paragraph(input[lastpos:i])
            start = i
        last ='n'
        lastpos = i
    elif c != ' ' and c != '\t':
        last = 'c'

process_paragraph(input[start:])
        
