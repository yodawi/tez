import hashlib, uuid, os
import hashlib
import MySQLdb
from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime
import calendar
import time
import base64


key = b'?\xfd\xc2\xba\x82\xe4\x8f/\x8f\x0c\xf6\xce\xd8x\xe1AY\xc3f\xcd\xa7n\x12\xbe@\xfe\xd0\xa2\xe6\x04l\x84'
pepper = b'\xcd\xe2a\r?Zvr\xa8\xeba\x83\xe0\x12\x9c\xe3q\xae_V\xf9\x81^\xbf@\xfb\xe7Z\x0b3e\x18'

conn = MySQLdb.connect(host='localhost', database='db')
app = Flask(__name__)

ttl = 3600
reload_ttl = 86400

t = datetime.utcnow().utctimetuple()

class User:
  email = str()
  password = str()
  token = str()
  
  hashed_password = bytes()

  def __init__(self, email='', password='', token=''):
    if email != '':
      self.email = email

    if password != '':
      self.password = password

    if token != '':
      self.token = token

  def hash(self):
    salt = hashlib.sha256(pepper + bytes(self.email, 'utf-8')).digest()

    self.hashed_password = salt + pepper + bytearray(self.password, 'utf-8')

    self.hashed_password = hashlib.sha512(self.hashed_password).digest()
    
    print(self.hashed_password)

  def save(self, force=False):
    try:
      r = conn.cursor()
      if force:
        r.execute('INSERT INTO Users (email, password) VALUES (LOWER(%s), %s) ON DUPLICATE KEY UPDATE email = LOWER(%s), password = %s', (self.email, self.hashed_password, self.email, self.hashed_password))
      else:
        r.execute('INSERT INTO Users (email, password) VALUES (LOWER(%s), %s)', (self.email, self.hashed_password))
      
      conn.commit()
      r.close()
      return True

    except:
      r.close()
      return False

  def verify(self):
    try:
      r = conn.cursor()
      
      r.execute('SELECT * FROM Users WHERE email=LOWER(%s) && password=%s;', (self.email, self.hashed_password))
      result = len(r.fetchall()) == 1

      r.close()
    
      return result

    except:
      r.close()
      return False
  
  def tokenize(self):
    data = (calendar.timegm(t) + ttl).to_bytes(4, byteorder='big', signed='false') + bytes(self.email, 'utf-8') + bytes(255 - len(self.email)) + self.hashed_password

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    token = cipher.nonce + tag + ciphertext

    return base64.b64encode(token)

  def decrypt(self):
    try:
      token = base64.b64decode(self.token)

      nonce = token[:16]
      tag = token[16:32]
      ciphertext = token[32:]


      cipher = AES.new(key, AES.MODE_EAX, nonce)
      data = cipher.decrypt_and_verify(ciphertext, tag)

      expiration = int.from_bytes(data[:4], "big")

      if expiration - ttl + reload_ttl <= calendar.timegm(t):
        return False

      self.email = data[4:259].decode("utf-8")
      self.email = self.email.rstrip('\x00')
      self.hashed_password = data[259:]

      return True

    except:
      return False





@app.route('/register', methods=['POST'])
def register():
  try:
    content = request.json
    email = content['email']
    password = content['password']

    if len(email)>255 :
      return 'Email is too long', 200

  except:
    return 'Invalid request', 200


  user = User(email=email, password=password)
  user.hash()
  
  if not user.save():
    return 'Email allready exists', 200
  
  else:
    return 'Success', 200


@app.route('/login', methods=['POST'])
def login():
  
  try:
    content = request.json
    email = content['email']
    password = content['password']

    if len(email)>255 :
      return 'Email is too long', 200

  except:
    return 'Invalid request', 200

  user = User(email=email, password=password)
  user.hash()
  
  if not user.verify():
    return 'Wrong', 200

  return user.tokenize(), 200


@app.route('/reload', methods=['POST'])
def _reload():
  try:
    content = request.json
    token = content['token']

  except:
    return 'Invalid request', 200

  user = User(token=token)
  user.decrypt()
  
  if not user.verify():
    return 'Wrong', 200

  return user.tokenize(), 200


@app.route('/change', methods=['POST'])
def change():
  try:
    content = request.json
    token = content['token']
    new_password = content['password']

  except:
    return 'Invalid request', 200

  user = User(token=token)
  user.decrypt()
  
  if not user.verify():
    return 'Wrong', 200

  user.password = new_password
  user.hash()

  user.save(force = True)

  return 'Success', 200

@app.route('/admin/upsert', methods=['POST'])
def upsert():
  try:
    content = request.json
    email = content['email']
    password = content['password']
    origin_verification = content['origin_verification']

    if origin_verification != 'bC+kuo/OPhCRPKoykaMflVLpyMx8lrchqrL/FOb/OSzvZbjP7JdO60NHdrg90UQCfQAe5NtJT/vB6R9KeCfyIg':
      return 'Invalid request', 200

    if len(email)>255 :
      return 'Email is too long', 200

  except:
    return 'Invalid request', 200


  user = User(email=email, password=password)
  user.hash()
  
  user.save(force = True)
    
  return 'Success', 200




if __name__ == "__main__":
  app = create_app()
  app.run()