import codecs
import json
import os
import re
import time
import urllib.request

class StatusMessage:
    """Status messages to display and read out loud to the user."""
    msg = ""
    def add(self, m):
        self.msg = self.msg + m + "\n"
    def read_out(self):
        print(self.msg)
        os.system("say '" + self.msg + "'")
        self.msg = ""

def stop_data_fetch(bus_name, stop_num):
    """Fetch NextBus data for the line and stop number."""
    utf_decoder = codecs.getreader("utf-8")
    api_response = urllib.request.urlopen('http://restbus.info/api/agencies/actransit/routes/' + bus_name + '/stops/' + str(stop_num) + '/predictions')
    data = json.load(utf_decoder(api_response))
    return data

def prediction_extract(data):
    """Extract the next three prediction times from the JSON data."""
    next_times = []
    for p in data[0]['values']:
        if p['minutes'] > 60:
            break
        next_times.append(p['minutes'])
    return next_times

def speech_format(next_times):
    """Format the next time predictions prettily."""
    line = ""
    for t in next_times:
        line += (str(t) + ", ")
    line += " minutes."
    line = re.sub(', ([0-9]+),  ', ', and \g<1> ', line)
    return line

def say(line):
    """Give the lines to the OS to say."""
    print(line)
    os.system("say " + line)

def read_out_times():
    """Give the user an update on the current time predictions."""
    status = StatusMessage()
    data_F = speech_format(prediction_extract(stop_data_fetch('F', '0304910')))
    data_18 = speech_format(prediction_extract(stop_data_fetch('18', '0304910')))

    status.add("The F bus is coming in " + data_F)
    status.add("You could also take the 18 bus coming in " + data_18)
    status.read_out()

def main():
    """Read out bus time predictions every 5 minutes."""
    print("")
    read_out_times()
    print("Next update in 5 minutes...")
    time.sleep(300) # Sleep for 5 minutes
    main()

main()
