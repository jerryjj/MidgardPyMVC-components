import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons.i18n.translation import _

import midgardmvc.lib.helpers as h

import unicodedata, re

import time
from datetime import datetime, timedelta

from random import Random

def generatePassword(passwordLength):
    password = ''
    
    rng = Random()

    righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
    lefthand = '789yuiophjknmYUIPHJKLNM'
    allchars = righthand + lefthand
    
    for i in range(passwordLength):
        if i%2:
            password += rng.choice(lefthand)
        else:
            password += rng.choice(righthand)
    
    return password
    
    