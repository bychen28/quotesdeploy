from __future__ import unicode_literals
from django.db import models
from datetime import datetime,date
import re
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		name_regex = re.compile(r'^[a-zA-Z ]+$')
		errors = {}
		if len(postData['name']) < 4:
			errors['name'] = 'Name should be more than 3 characters'
		if len(postData['uname']) < 4:
			errors['uname'] = 'Username should be more than 3 characters'
		if not name_regex.match(postData['name']):
			errors['letters'] = 'Letters only for name please'
		if len(postData['pword']) < 8:
			errors['pword'] = 'Password should be atleast 8 characters'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'Passwords dont match'
		if User.objects.filter(username = postData['uname'].lower()).exists():
			errors['exists'] = 'Username already used'
		if len(postData['date']) == 0:
			errors['date'] = "Birthday Field Cannot be Empty"
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			a = User.objects.create(name = postData['name'], username = postData['uname'],
				pword = pw)
			errors['id'] = a.id
		return errors

	def login_validator(self,postData):
		errors = {}
		if len(postData['luname']) < 4:
			errors['luname'] = 'Username should be atleast 3 characters'
		if len(postData['lpword']) < 8:
			errors['lpword'] = 'Password should be atleast 8 characters'
		if len(errors) == 0:
			if User.objects.filter(username = postData['luname']).exists():
				a = User.objects.get(username = postData['luname'])
				if bcrypt.checkpw(postData['lpword'].encode(), a.pword.encode()):
					errors['id'] = a.id
				else:
					errors['credentials'] = "Wrong Credentials"
			else:
				errors['credentials'] = "Wrong Credentials"
		return errors

class QuoteManager(models.Manager):
    def validate_quote(self,postData):
		errors = {}
		if len(postData['quotedby']) < 4:	
			errors['quotedby'] = 'Quoted by field must be more than 4 Characters'
		if len(postData['quotetext']) < 10:
			errors['quotetext'] = "Quote Field Must be more than 10 Characters"
		if len(errors) == 0:
			userquote = Quote.objects.create(quoted_by=postData['quotedby'],quote_text=postData['quotetext'],added_by_id = postData['uid'])
			errors['success'] = 'Sucessfully Added a Quote'
		return errors
    
class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	pword = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	objects = UserManager()

class Quote(models.Model):
	quoted_by = models.CharField(max_length=255)
	quote_text = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	added_by = models.ForeignKey(User, related_name= "posted_quote")
	favorite_quotes = models.ManyToManyField(User, related_name="favorited_quotes")
	objects = QuoteManager()