#!/usr/bin/env python2.7

# Copyright 2013
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import smtplib, string, subprocess, time, socket, re,urllib2

# Import ./settings.py file
# If this fails for you, copy settings_example.py to settings.py and change the values
import settings

def get_ifconfig():
    request = urllib2.Request("http://www.whereismyip.com/")
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
    readhttp=urllib2.urlopen(request,timeout=10).read()
    ip=re.search('\d+\.\d+\.\d+\.\d',readhttp).group(0)
    return ip

    

def send_mail(settings, BODY):
    try:
        server = smtplib.SMTP(settings.server)
        server.starttls()
        server.login(settings.u, settings.p)
        server.sendmail(settings.fromaddr, settings.toaddr, BODY)
        server.quit()
    except socket.gaierror:
        print("Couldn't connect to SMTP, trying again in a minute ...")
        time.sleep(60)
        send_mail(settings, BODY)

ifconfig = get_ifconfig();
while (not ifconfig[0]):
    print("Could not determine IP, waiting to retry ...")
    time.sleep(1)
    ifconfig = get_ifconfig()

BODY = string.join((
"From: %s" % settings.fromaddr,
"To: %s" % settings.toaddr,
"Subject: Your RasberryPi just booted at " + time.ctime(),
"",
ifconfig,
), "\r\n")

print("Sending email ...")
send_mail(settings, BODY)

