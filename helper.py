import re
import os
import binascii
import db as database

class InputParser(object):
    regex = {
        'hostname': r'''^[-a-zA-Z0-9_]{1,32}$''',
        'key': r'''^([a-fA-F0-9]{64})?$''',
        'email': r'''^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$''',
        'nickname': r'''^[-a-zA-Z0-9_ äöüÄÖÜß]{1,64}$''',
        'mac': r'''^([a-fA-F0-9]{12}|([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2})$''',
        'coords': r'''^(-?[0-9]{1,3}(\.[0-9]{1,15})? -?[0-9]{1,3}(\.[0-9]{1,15})?)?$'''
    }

    def __init__(self):
        pass

    def __normalizeStrings(self, struct):
        return dict((k.lower(), v) for k, v in struct.items())

    def getData(self, req):
        res = self.__normalizeStrings(req.form.to_dict())
        return res

    def __validationError(self, vres):
        res = {}
        res['status'] = 'error'
        res['type'] = 'ValidationError'
        res['validationResult'] = vres
        return res

    def validate(self, req):
        invalid = []
        missing = []
        unknown = []
        errors = False
        res = {}
        data = self.getData(req)

        for key in self.regex.keys():
            if not data[key]:
                missing.append(key)
                errors = True

        for key in data.keys():
            value = data[key]
            if key not in self.regex.keys():
                unknown.append(key)
                errors = True
            elif not re.search(self.regex[key], value, re.MULTILINE):
                invalid.append(key)
                errors = True

        res['invalid'] = invalid
        res['missing'] = missing
        res['unknown'] = unknown
        res['hasErrors'] = errors

        if errors:
            return self.__validationError(res)
        else:
            return None

class Token(object):
    def getToken(self):
        return binascii.b2a_hex(os.urandom(15)).decode('utf-8')

class Dedup(object):
    db = database.DB()
    def checkDups(self, hostname, mac, key):
        if self.db.checkHostname(hostname):
            return {'status':'error', 'type':'NodeEntryAlreadyExistsError','hostname': hostname}
        elif self.db.checkMAC(mac):
            return {'status':'error', 'type':'MacEntryAlreadyExistsError','mac': mac}
        elif self.db.checkKey(key):
            return {'status':'error', 'type':'KeyEntryAlreadyExistsError','key': key}
        else:
            return None
