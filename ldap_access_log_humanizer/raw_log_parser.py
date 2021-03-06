import re
from ldap_access_log_humanizer.custom_logger import CustomLogger


class RawLogParser:
    def __init__(self, args_dict):
        self.args_dict = args_dict
        self.logger = CustomLogger(self.args_dict)

    def parse(self, line):
        # This regex takes a raw log and parses it into a few elements
        # time, server, process, and arbitrary remainder
        pattern = r'^(\w+ +\d+ \d+:\d+:\d+) ([a-zA-Z0-9\.]+) (\w+\[\d+\]): conn=(\d+) (.*)$'
        match = re.search(pattern, line)

        if match:
            return {'time': match.group(1),
                    'server': match.group(2),
                    'process': match.group(3),
                    'conn': match.group(4),
                    'rest': match.group(5)}
        else:
            # raise Exception('Failed to parse raw line: {}'.format(line))
            if self.args_dict['verbose']:
                self.logger.log("ERROR: Failed to parse raw line: {}".format(line), error=True)
            return None
