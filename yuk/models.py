from django.db import models
from django.forms import ModelForm
from django import forms
from tagging.forms import Tag, TagField
from urlparse import urlparse, urlunparse
import sys

class MyUrlField(forms.URLField):

        def to_python(self, value):
                '''Lowercase the URL input for validation.'''
                if value.startswith('http://') or value.startswith('https://'):
                        return self.lowercase_domain(value)
                else:
                        return self.lowercase_domain('http://%s' % value)

        def lowercase_domain(self, url):
                parsed = urlparse(url)
                retval = urlunparse((parsed.scheme,
                                     parsed.netloc.lower(),
                                     parsed.path,
                                     parsed.params,
                                     parsed.query,
                                     parsed.fragment))
                if url.endswith('?') and not retval.endswith('?'):
                        retval += '?'
                return retval
                

class Url(models.Model):

        def __unicode__(self):
                return self.url

        url = models.URLField(unique=True)
        url_name = models.CharField(max_length=200)
        tagstring = models.CharField(max_length=200)
        url_desc = models.TextField()

        def save(self):
                super(Url, self).save()
                self.tags = self.tagstring

        def _get_tags(self):
                return Tag.objects.get_for_object(self)

        def _set_tags(self, tagstring):
                Tag.objects.update_tags(self, tagstring)

        tags = property(_get_tags, _set_tags)

	
        
class UrlForm(ModelForm):
        url = MyUrlField(label='URL:')
	url_name = forms.CharField(label='Name:', required=False)
	tagstring = forms.CharField(label='tags separated by commas:', required=False)
	url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea, required=False)
        class Meta:
                model = Url

