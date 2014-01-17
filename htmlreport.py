import sys
import re
from datetime import datetime
from collections import defaultdict
from log_parsing import *

def dump_events_to_html(filename, events):
    h = open("results.html" ,"w")
    print >> h,  """<html>
                      <head>
                        <title>Results from log: """ + filename + """</title>
                        <link rel="stylesheet" type="text/css" href="./results.css"/>
                      <body><ul>"""
    for e in events:
        print >> h, "<li>", "<span class='time'>", e.short_time_str, "</span>", 
        print >> h, "<span class='name'>", e.name, "</span>", 
        print >> h, "<span class='attributes'>" 
        for name in e.event_class.attributes:
            value = getattr(e, name)
            if value:
                print >> h, "<span class='aname'>", name, "</span>: <span class='avalue, attr-" + name + "'>", value, "</span>"

        print >> h, "</span>", "</li>"

    print >> h, "</ul></body></html>"

def dump_groups_to_html(filename, groups):
    h = open("groups.html" ,"w")
    print >> h,  """<html>
                      <head>
                        <title>Results from log: %s</title>
                        <link rel="stylesheet" type="text/css" href="./results.css"/>
                      <body>""" % (filename)
    for ssid, events in groups.items():
        print >> h, "<span class='group'>%s</span><ul>" % (ssid)
        for e in events:
            print >> h, "<li>", "<span class='time'>", e.short_time_str, "</span>", 
            print >> h, "<span class='logger'>%s</span>: <span class='name'>%s</span>" % (e.logger, e.name) 
            print >> h, "<span class='attributes'>" 
            for name in e.event_class.attributes:
                value = getattr(e, name)
                if name != "subscription_id" and value:
                    print >> h, "<span class='aname'>%(name)s</span>: <span class='avalue, attr-%(name)s'>%(value)s</span>" % dict(name=name, value=value)
            print >> h, "</span>", "</li>"
        print >> h, "</ul>"

    print >> h, "</body></html>"
