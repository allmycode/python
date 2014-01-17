import sys, re, datetime

# This script checks if date interval between heartbeat messages is
# more than 5 second
FILE = 'ospe-bb-server-1.log'
PATTERN = r'(\w{3} \d \d{2}:\d{2}:\d{2}.\d{3})'
DATE_FORMAT = '%b %d %H:%M:%S.%f'
INTERVAL = 5

f = open(FILE, 'r')
p = re.compile(r'\[OSPE-1\] ' + PATTERN + '  INFO - Publishing availability heartbeat AVAILABLE \[\] \[BuildingBlockLifecycleImpl\] \[bb-lifecycle-executor1\]')
tp = None
for line in f:
    m = re.match(p, line)
    if m:
        t = datetime.datetime.strptime(m.groups()[0], DATE_FORMAT)
        if tp and (t - tp).seconds > INTERVAL:
            print "Alert:" + str(t) + " - " + str(tp) + " is more than " + str(INTERVAL) + " seconds"
        tp = t
