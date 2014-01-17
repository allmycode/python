import sys, os

def main(args):
    for file in args:
        count = 0
        for char in open(file).read():
            count += 1
        print file + " has " + str(count) + " chars"

if __name__ == "__main__":
    main(sys.argv)
