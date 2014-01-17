import sys
import re
from datetime import datetime
from collections import defaultdict
from log_parsing import *
from htmlreport import *

sonic_int_subscribed = EventClass("Sonic-int subscribed", r"New client subscribed, subscription=(?P<subscription_id>\S+),")

sonic_int_unsubscribed = EventClass("Sonic-int unsubscribed", "Client unsubscribed, subscription=(?P<subscription_id>\S+),")

sonic_subscribed = EventClass("Sonic subscribed", "Subscription(?: for (?P<streaming_id>\d+))? succeeded\. (?:Sonic s|S)ubscription ID is (?P<subscription_id>\S+)")
sonic_unsubscribe = EventClass("Sonic unsubscribe", "Unsubscribing from Sonic: (?P<subscription_id>\S+)")

user_request = EventClass("User request", "Received request from UserSession \[sessionId=(?P<session_id>\d+), userId=(?P<user_id>[^,]+).*\] : (?P<request>.*)")
user_subscription_request = EventClass("User subscription request", "Received subscription request from UserSession \[sessionId=(?P<session_id>\d+), userId=(?P<user_id>[^,]+).*\] : (?P<request>.*)")

user_response = EventClass("User response", "Returning response to UserSession \[sessionId=(?P<session_id>\d+), userId=(?P<user_id>[^,]+).*\] : (?P<response>.*)")
subscription_added = EventClass("Subscription added", "Subscription id: (?P<streaming_id>\d+) revision: (?P<revision>\d+) is added for session ID (?P<session_id>\d+)\.")
ladder_selected = EventClass("Ladder selected", "Sonic ladder id for subscription (?P<streaming_id>\d+) \[pricing session id (?P<pricing_session_id>\d+)\]: (?P<ladder>.*)")

sonic_subs_price = EventClass("Price", "Subscription \[(?P<streaming_id>\d+) (?P<pricing_session_id>\d+) (?P<client_id>.*)\]: SonicUpdate .*Premium=(?P<premium>.*\]\]), Premi.*SubscriptionId=(?P<subscription_id>[^,\]]*)")
sonic_vals_price = EventClass("Resolve price", "Values Service subscription \[(?P<subscription_id>\S+) (?P<client_id>[^\]]*)\]")

class Streaming(list):
    def __init__(self):
        self.streaming_id = None
        self.user_id = None
        self.ladder = None
        self.sonic_subs = 0
        self.lived = 0
    
    def append1(self, e):
        list.append(self, e)
        if hasattr(e, 'name'):
            if e.event_class == subscription_added:
                self.streaming_id = e.streaming_id
            if e.event_class == ladder_selected:
                self.ladder = e.ladder
            if e.event_class == user_subscription_request:
                self.user_id = e.user_id

    def getall(self):
        for e in self:
            if not hasattr(e, 'name'):
                for se in e:
                    self.append1(se)
                self.remove(e)
        self.sort(key=lambda o: o.time)
        self.time = self[0].time

    def check_health(self):
        subs = None
        for e in self:
            if e.event_class == sonic_subscribed:
                subs = e
            if e.event_class == sonic_subs_price:
                if subs:
                    diff = e.time - subs.time
                    if diff.total_seconds() > 10:
                        print "Found " + str(self.streaming_id)
                        subs.health = "Long subscription " + str(diff.total_seconds()) + " seconds"
                        if not hasattr(self, 'health'):
                            self.health = ""
                        self.health += subs.health + " "
                    subs = None
        

def main(args):
    dir = "c:/local/tmp/uat9";
    filename = "c:/local/tmp/uat9/ospe-bb-server-1.log"
    pricesfilename = "c:/local/tmp/uat9/ospe-bb-server-1_sonic_price.log"

    log = LogFile(filename, BaseLog(), 
                  [sonic_int_subscribed, sonic_int_unsubscribed, sonic_subscribed, sonic_unsubscribe, 
                   user_subscription_request, user_request, user_response, subscription_added, ladder_selected])


    prices = LogFile(pricesfilename, BaseLog(), 
                     [sonic_subs_price, sonic_vals_price])

    for m in prices.m[:10]:
        print m

    last_user_subscription_requests = {}
    streamings = defaultdict(Streaming)
    sonic_ints = defaultdict(list)
    for e in log.events:
        if e.event_class == user_subscription_request:
            last_user_subscription_requests[(e.thread, e.session_id)] = e
        if e.event_class == subscription_added:
            streamings[e.streaming_id].append1(e);
            ur = last_user_subscription_requests.get((e.thread, e.session_id))
            if ur:
                streamings[e.streaming_id].append1(ur);
        if e.event_class == ladder_selected:
            if streamings.has_key(e.streaming_id):
                streamings[e.streaming_id].append1(e);
            else:
                print >> sys.stderr, "Ladder found, but no streaming " + e.streaming_id
        if e.event_class == sonic_subscribed:
            streamings[e.streaming_id].append1(e);
            streamings[e.streaming_id].append1(sonic_ints[e.subscription_id])

        if e.event_class == sonic_unsubscribe:
            sonic_ints[e.subscription_id].append(e)        
        if e.event_class == sonic_int_subscribed:
            sonic_ints[e.subscription_id].append(e)
        if e.event_class == sonic_int_unsubscribed:
            sonic_ints[e.subscription_id].append(e)

    for p in prices.events:
        sonic_ints[p.subscription_id].append(p) 

    for sid, elist in streamings.items():
        elist.getall()
        elist.check_health()

    h = open(dir + "/streamings.html" ,"w")
    h.write("""<html><head><title>%s</title><link rel="stylesheet" type="text/css" href="results.css"/><head></body>""" % filename)
    h.write("<h2>Total streamings: %d</h2>" % len(streamings))
    for sid, elist in sorted(streamings.items(), key=lambda(k,v): v.time):
#        print "Streaming: " + str(sid) + " user: " + str(elist.user_id)
        h.write("<h3>Streaming " + str(sid) + " user: " + str(elist.user_id) +"</h3><ul>")
        if hasattr(elist, 'health'):
            h.write("<span class='warn'>%s</span>" % elist.health)
        for e in elist:
            h.write("<li>%s <span class='ename'>%s</span> " % (e.short_time_str, e.name))
            if hasattr(e, 'health'):
                h.write("<span class='warn'>%s</span>" % e.health)
            for name in e.event_class.attributes:
                value = getattr(e, name)
                if value:
                    h.write("<span class='aname'>%(name)s</span>: <span class='avalue, attr-%(name)s'>%(value)s</span> " % dict(name=name, value=value))

            h.write("</li>")
        h.write("</ul>")

    h.write("</body></html>")
            

if __name__ == "__main__":
    main(sys.argv)
