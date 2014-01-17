import sys
import re
from datetime import datetime
from collections import defaultdict

class LogFormat:
    def __init__(self, record_regex):
        self.record_regex = re.compile(record_regex)

    def process_attributes(self, attributes):
        return attributes

class BaseLog(LogFormat):
#[OSPE-1] Nov 8 15:26:51.198  INFO - Unsubscribing from Sonic: f0437503-1f1a-433f-924d-1d99c1b999b2@e1854845-f2bf-4e03-b24f-2f6c35aec0ac [] [StreamingServiceImpl] [ospe-streaming-thread-pool17-2]
    def __init__(self):
        LogFormat.__init__(self, r"^\[(?P<bb>.*)\] (?P<time>\w{3} \d{1,2} \d\d:\d\d:\d\d.\d\d\d)\s+(?P<level>\w+) - (?P<record>.*) \[.*\] \[(?P<logger>\w+)\] \[(?P<thread>\S+)\]$")

    def process_attributes(self, attributes):
        attributes = LogFormat.process_attributes(self, attributes)
        attributes['time'] = datetime.strptime(attributes['time'], "%b %d %H:%M:%S.%f")
        return attributes
        
class LogFile:
    def __init__(self, filename, logformat, event_classes):
        self.filename = filename
        self.logformat = logformat
        self.event_classes = event_classes
        self.events = list()
        self.m = []
        self.process_events()

    def process_events(self):
        print "Going to process file: " + self.filename
        log = open(self.filename)
        count = 0
        for line in log:
            count += 1
            lo = self.logformat.record_regex.match(line)
            if lo:
                text = lo.group('record')
                for ec in self.event_classes:
                    mo = ec.get_matcher(text)
                    if mo:
                        self.events.append(Event(ec, line, self.logformat.process_attributes(lo.groupdict()), ec.process_attributes(mo.groupdict()))) 
            else:
                self.m.append(line)
                
        print "Proccesed lines: " + str(count) + ", found events: " + str(len(self.events))
        log.close()

    def print_total_by_classes(self):
        counts = defaultdict(lambda: 0)
        for e in self.events:
            counts[e.name] += 1
        for name, count in counts.items():
            print name, count

class Event:
    def __init__(self, event_class, logline, system_attributes, attributes):
        self.name = event_class.name
        self.event_class = event_class
        self.logline = logline
        for sname, svalue in system_attributes.items():
            setattr(self, sname, svalue)
        self.short_time_str  = datetime.strftime(self.time, "%H:%M:%S")
        for name, value in attributes.items():
            setattr(self, name, value)

class EventClass:
    def __init__(self, name, regexstr):
        self.name = name
        self.pattern = re.compile(regexstr)
        self.attributes = self.pattern.groupindex.keys() 

    def get_matcher(self, text):
        return self.pattern.search(text)

    def process_attributes(self, attrs):
        return attrs
