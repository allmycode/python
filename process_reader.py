import subprocess

bla = subprocess.Popen(["python", "bla.py"], shell=True, stdout=subprocess.PIPE)

print "Stating output..."
while True:
    print(bla.stdout.readline())

print "Finished"
