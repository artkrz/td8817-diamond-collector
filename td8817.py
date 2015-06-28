#!/usr/bin/python

import re
import telnetlib
import diamond.collector

class TD8817Collector(diamond.collector.Collector):
    def collect(self):
        PROMPT = 'TP-LINK>'
	HOST = '192.168.1.1'
	PASSWORD = '...'
        tn = telnetlib.Telnet(HOST)
	tn.read_until('Password: ')
	tn.write(PASSWORD + '\n')
        tn.read_until(PROMPT)
	tn.write('w ad perfdata\n')
        output = tn.read_until(PROMPT)
	tn.write('wan adsl c\n')
        output += tn.read_until(PROMPT)
	tn.write('exit\n')

	for line in output.splitlines():
	    if "ADSL" in line:
	        continue
	    m = re.match("([A-Za-z- 0-9]+)\s*:\s*([0-9]+)", line)
	    if m:
	        metric = m.group(1)
	        metric = metric.rstrip()
	        metric = metric.replace(" ", ".")
	        value = m.group(2)
                self.publish(metric.lower(), value, precision=0)

