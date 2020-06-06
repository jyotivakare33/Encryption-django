#from django.db import models


from mongoengine import Document,StringField,IntField,EmailField,BinaryField



class User(Document):

    first_name = StringField(max_length=20)
    last_name  = BinaryField(max_length=500)
    contact    = StringField(max_length=40)
    email      = StringField(max_length=50)

    meta = {
        'indexes':['first_name','last_name'],
        'ordering':['-date_created']
    }




