import re
#[OSPE-1] Nov 8 15:26:51.198  INFO - Unsubscribing from Sonic: f0437503-1f1a-433f-924d-1d99c1b999b2@e1854845-f2bf-4e03-b24f-2f6c35aec0ac [] [StreamingServiceImpl] [ospe-streaming-thread-pool17-2]

logrecord_pattern_str = r"^\[(?P<bb>.*)\] (?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d.\d\d\d)\s+(?P<level>\w+) - (?P<record>.*) \[.*\] \[(?P<logger>\w+)\] \[(?P<thread>\S+)\]$"

log = open(r"c:/dev/abfx2/trunk/options/ospe-bb/configuration/target/ospe-bb-configuration-13.3.8-SNAPSHOT-local-package/log/ospe-bb-server-1.log")
r = re.compile(logrecord_pattern_str) 
r2 = re.compile("Subscription(?P<bla>.*) succeeded")
c = 0
for line in log:
    mo = r.match(line)
    if mo:
        c+=1
        ro = r2.search(mo.group('record'))
        if ro:
            print ro.groupdict()

print c

