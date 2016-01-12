from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class turl(models.Model):
	urlid= models.AutoField(primary_key=True)
	url = models.CharField(max_length=1000)
	surl = models.CharField(max_length=10)
	title = models.CharField(max_length=2000)
	hits = models.IntegerField(default=0)

	def __str__(self):
		return str(self.urlid)
