from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
    
    def __unicode__(self):
        return self.user.username

class Project(models.Model):
    projID = models.AutoField(primary_key=True)
    projName = models.CharField(max_length=128, unique = True)
    description = models.TextField(null=True)
    enrollmentKey = models.CharField(max_length=128)

    def __unicode__(self):
        return self.projName

class Category(models.Model):
    cateID = models.AutoField(primary_key=True)
    cateName = models.CharField(max_length=128, unique = True)

    def __unicode__(self):
        return self.cateName

class Specification(models.Model):
    attrID = models.AutoField(primary_key=True)
    attrTitle = models.CharField(max_length=128, unique = True, null = False)
    priority = models.IntegerField()
    attrDate = models.DateField()
    attrDesc = models.TextField(null=True)
    flag = models.BooleanField(default=False)
    projID = models.ForeignKey('Project')
    cateID = models.ForeignKey('Category')

    def __unicode__(self):
        return self.attrTitle

class Lead(models.Model):
    leader = models.ForeignKey(User)
    projects = models.ForeignKey('Project')
    
    def __unicode__(self):
        return unicode(self.leader) or u''

class Join(models.Model):
    users = models.ForeignKey(User)
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return unicode(self.project) or u''
