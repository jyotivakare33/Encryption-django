from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseNotFound 
from django.template import loader 
from myFirstApp.models import User
from django.core.exceptions import ObjectDoesNotExist
import base64
import os
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

password = "value"


def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = os.urandom(16)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def index(request):
    name=''
    encrypted= '';
    if request.method == 'POST':
        encrypted = encrypt(request.POST['last_name'],password);
        newUser = User(first_name = request.POST['first_name'])
        newUser.last_name = encrypted
        newUser.contact = request.POST['contact']
        newUser.email = request.POST['email']
        newUser.save()

    name = decrypt(encrypted,password)
    params = {'user':User.objects}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(params))




     