BUFFER_SIZE = 512
SEPARATORS = {' ', '\t', '\n', ':', '(', ')', "'", '"', '\\', ',', '.', '+', '=', '-', ']', '[', 
              '>', '<', '{', '}', ';', '|', '!', '?', '&', '%'}

def index_file(filename):
    wordmap = {}
    buf = file.read(BUFFER_SIZE)
    word = ""
    while buf:
        i = 0
        while i < len(buf):
            if buf[i] not in SEPARATORS: 
                word += buf[i]
            else:
                if word:
                    count = wordmap.get(word)
                    if not count: wordmap[word] = 0
                    wordmap[word] += 1
                    word = ""
            i += 1
        buf = file.read(BUFFER_SIZE)

    if word:
        count = wordmap.get(word)
        if not count: wordmap[word] = 0
        wordmap[word] += 1

    return wordmap


def main(path):
    import os
    if os.path.isfile(path):
        
    
if __name__ == "__main__":
    from sys import argv
    main(*argv):
