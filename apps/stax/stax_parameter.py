from datetime import datetime
import re

class StaxParameter:
    def __init__(self, name, param_type, default=None, validator=None):
        self.name = name
        self.type = param_type
        self.default = default
        self.validator = validator
        if not validator:
            if self.type == 'number':
                self.validator = self.number_validator
            elif self.type == 'date':
                self.validator = self.date_validator
            elif self.type == 'datetime':
                self.validator = self.datetime_validator
            elif self.type == 'time':
                self.validator = self.time_validator
            elif self.type == 'email':
                self.validator = self.email_validator
            elif self.type == 'url':
                self.validator = self.url_validator
            elif self.type == 'color':
                self.validator = self.color_validator
        if self.validator and default and not self.validate(default):
            raise ArgumentError('Default value')

    def validate(self, value):
        if not self.validator:
            return True
        return self.validator(value)

    def date_validator(self, d):
        try:
            datetime.strptime(d, '%m/%d/%Y')
            return True
        except ValueError:
            return False

    def datetime_validator(self, d):
        try:
            datetime.strptime(d, '%m/%d/%Y %I:%M %p')
            return True
        except ValueError:
            return False

    def email_validator(self, e):
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match("foo@bar.com") is not None

    def url_validator(self, u):
        url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_regex.match(u) is not None

    def number_validator(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    def time_validator(self, t):
        try:
            datetime.strptime(d, '%I:%M %p')
            return True
        except ValueError:
            return False

    def color_validator(self, c):
        color_regex = re.compile(r'#[a-f0-9]{6}')
        return color_regex.match(c) is not None
