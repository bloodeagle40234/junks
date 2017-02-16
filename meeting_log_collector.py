from html.parser import HTMLParser
import requests
from datetime import datetime
import os

LOG_HOST = 'http://eavesdrop.openstack.org'

class LinkParser(HTMLParser, object):
    def __init__(self):
        super(LinkParser, self).__init__()
        self.href_attrs = []

    def handle_starttag(self, tag, attrs):
        if 'a' in tag and attrs:
            attr, link = attrs[0]
            if attr == 'href':
                self.href_attrs.append(link)


class NormalLogParser(object):
    # NOTE: channel should not starts with slash
    channel = 'irclogs/%23openstack-swift/'
    base_url = 'http://eavesdrop.openstack.org/irclogs/%23openstack-swift/'
    name_wrap = '%s'
    log_ext = 'log.html'

    @property
    def base_url(self):
        return os.path.join(LOG_HOST, self.channel)

    def latter_than(self, base_datetime, log_name):
        # log name should be like swift.2016-09-07-21.00.log.txt
        if log_name == 'latest.log.html':
            return False
        date_str = log_name.split('.')[1]
        # print date_str 
        parsed = self.split_log_date(date_str)
        log_date = datetime(
            year=int(parsed[0]), month=int(parsed[1]), day=int(parsed[2]))
        return log_date > base_datetime

    def split_log_date(self, date_str):
        return date_str.split('-', 3)

    def ext_check(self, log_name):
        return log_name.endswith(self.log_ext)

    def wrap_name(self, name):
        return self.name_wrap % name


class MeetingLogParser(NormalLogParser):
    channel = 'meetings/swift/2016/'
    name_wrap = '<%s>'
    log_ext = 'log.txt'

    def split_log_date(self, date_str):
        return date_str.split('-', 4)


def collect_my_voice(whoami, logs):
    voices = []
    for alog in logs:
        resp = requests.get(alog)
        for line in resp.content.split('\n'):
            if whoami in line:
                voices.append(line)
    return voices


if __name__ == '__main__':
    log_parser = MeetingLogParser()
    # log_parser = NormalLogParser()
    resp = requests.get(log_parser.base_url)
    parser = LinkParser()
    parser.feed(resp.content)
    base_datetime = datetime(year=2016, month=4, day=1)
    logs = [os.path.join(log_parser.base_url, item) for item in parser.href_attrs
            if log_parser.ext_check(item) and log_parser.latter_than(base_datetime, item)]
    voices = collect_my_voice(log_parser.wrap_name('kota_'), logs)
    print '# of join: %s' % len(logs)
    print '# of voices: %s' % len(voices)
    print voices
