#!/usr/bin/python
# To run this program you should install python 2.7
# and type in command line > python just.py <input_file> <output_file> [<columns>=80]

def format(acc, out, red, N):
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

def format_paragraph(p, output, N):
#    print "Processing: ", p
    acc = list()
    chars = 4
    red = True
    for w in p.split():
        if len(w) + chars + 1 > N:
            format(acc, output, red, N)
            if red: red = None
            acc = list()
            chars = 0
        acc.append(w)
        chars += len(w) + 1
    format(acc, output, red, N)
    return output

def format_text(input, output, N):
    start = 0
    lastpos = -1;
    last = None
    for i, c in enumerate(input):
        if c == '.':
            last = 'd'
            lastpos = i 
        elif c == '\n':
            if last == 'd':
                format_paragraph(input[start:lastpos+1], output, N)
                start = i
            elif last == 'n':
                format_paragraph(input[start:lastpos], output, N)
                if i - lastpos > 1: 
                    format_paragraph(input[lastpos:i], output, N)
                    start = i
            last ='n'
            lastpos = i
        elif c != ' ' and c != '\t':
            last = 'c'

    format_paragraph(input[start:], output, N)
    return output

def main():
    from sys import argv, stdout

    input = open(argv[1] if len(argv) > 1 else 'lorem.txt').read()
    output = open(argv[2], 'w') if len(argv) > 2 and argv[2] != '-' else stdout
    N = int(argv[3]) if len(argv) > 3 else 80    
    
    format_text(input, output, N)

def test_format_paragraph(text, N):
    from StringIO import StringIO
    return format_paragraph(text, StringIO(), N).getvalue()

def check(val, expected):
    assert val == expected, "'"+val+"' != '"+expected+"'"
    
def tests():
    check(test_format_paragraph('Lorem ipsum', 80), '    Lorem ipsum\n')
    check(test_format_paragraph('Lorem ipsum', 20), '    Lorem      ipsum\n')

if __name__ == "__main__":
    #tests()
    main()
        
