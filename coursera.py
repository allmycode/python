import urllib2
import urllib

base_page="https://www.coursera.org/"


login_url = "https://www.coursera.org/maestro/api/user/login"
post_params = {
"signin-email": "stas.lyahnovich@gmail.com",
"signin-password": "wer311"}
post_data = urllib.urlencode(post_params)
headers = {"Referer": "https://www.coursera.org/account/signedin",
           "Origin":"https://www.coursera.org",
           "Host":"www.coursera.org"}

try:
    login_request = urllib2.Request(login_url, post_data, headers)
    login_response = urllib2.urlopen(login_request)
except urllib2.HTTPError as e:
    import re
    re_search = re.search("<div id=\"summary\">(.*)</div>", e.read(), re.DOTALL)
    reason = "\n" + re_search.group(1).strip() if re_search else ""
    print(str(e.code) + ": " + e.reason + reason)
