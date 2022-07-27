import hashlib, uuid, os
from random import randbytes
import hashlib

from paramiko import PasswordRequiredException

pepper = b'\xcd\xe2a\r?Zvr\xa8\xeba\x83\xe0\x12\x9c\xe3q\xae_V\xf9\x81^\xbf@\xfb\xe7Z\x0b3e\x18'

users_database = []

class User:
  email = str()
  password = str()

  salt = bytes()
  hashed_password = bytes()

  def __init__(self, email, password):
    self.email = email
    self.password = password

  def hash(self):
    #self.salt = os.urandom(32)
    self.salt = hashlib.sha256(pepper + bytes(self.email, 'utf-8')).digest()

    self.hashed_password = self.salt + pepper + bytearray(self.password, 'utf-8')

    self.hashed_password = hashlib.sha512(self.hashed_password).digest()

  def save(self):
    #data = bytes([len(self.email)]) + bytes(self.email, 'utf-8') + self.salt + self.hashed_password
    data = {"email": self.email, "salt": self.salt, "hashed_password": self.hashed_password}

    return(data)

  def find(self):
    global users_database

    #for usr in users_database:

    #get({"email": self.email, "salt": self.salt, "hashed_password": self.hashed_password})

    print(len(self.salt), len(self.hashed_password))
    return(0)




def create_user(request):
  try:
    content = request#.json
    email = content['email']
    password = content['password']

    if len(email)>255 :
      return {'error': 'Email is too long'}
  except:
    return {'error': 'Invalid request'}

  global users_database

  user = User(email, password)
  user.hash()
  users_database = users_database + [user.save()] # test

def login_user(request):
  try:
    content = request#.json
    email = content['email']
    password = content['password']

    if len(email)>255 :
      return {'error': 'Email is too long'}
  except:
    return {'error': 'Invalid request'}

  user = User(email, password)
  user.hash()
  
  return user.find()
  


create_user({"email": "rafafoxbrasil9@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil2@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil3@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil4@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil5@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil6@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil7@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil8@gmail.com", "password": "Passsword$"})
create_user({"email": "rafafoxbrasil1@gmail.com", "password": "Passsword$"})

login_user({"email": "rafafoxbrasil9@gmail.com", "password": "Passsword$"})
