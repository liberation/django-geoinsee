# -*- coding: UTF-8 -*-
import re
import math
import unicodedata

EARTH_RADIUS_KM = 6371.0


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) \
        + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) \
        * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_RADIUS_KM * c
    return d


def normalize_text(string):
    """ retire les accents d'une string
    en cas d'erreur la valeur de la string
    originale est retournée"""
    try:
        return unicodedata.normalize(
            'NFKD', u'%s' % string).encode('ascii', 'ignore')
    except:
        return string


def slugifyfr(value):
    """Converts to lowercase, removes
    non-alpha chars and converts spaces to hyphens"""
    try:
        value = normalize_text(value).strip().lower()
        value = re.sub('[\W\s]', '-', value)
        value = re.sub('([-]{1}[a-z|0-9]{1})(?![a-z|0-9])', '-', value)
        value = re.sub('(^[a-z|0-9]{1}[-]{1})', '-', value)
        value = re.sub('[-]{2,}', '-', value)
        value = re.sub('-$', '', value)
        value = re.sub('^-', '', value)
        return value
    except:
        return value
