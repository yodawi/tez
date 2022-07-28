import hashlib
from Crypto.Cipher import AES
import calendar
from datetime import datetime
import requests
import json
import base64

key = b'?\xfd\xc2\xba\x82\xe4\x8f/\x8f\x0c\xf6\xce\xd8x\xe1AY\xc3f\xcd\xa7n\x12\xbe@\xfe\xd0\xa2\xe6\x04l\x84'
t = datetime.utcnow().utctimetuple()

def verifyToken(token):
  try:
    token = base64.b64decode(token)

    nonce = token[:16]
    tag = token[16:32]
    ciphertext = token[32:]


    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    timestamp = data[:4]
    email = data[4:259]

    expiration = int.from_bytes(timestamp, "big")
    email = email.decode("utf-8")

    if expiration <= calendar.timegm(t):
      return False
    
    return email
  
  except:
    return False