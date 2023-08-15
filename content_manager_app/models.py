from django.utils import timezone
from django.db import IntegrityError, models

class EntryTracker(models.Model):
    item_id = models.IntegerField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    lock = models.CharField(max_length=1, null=False, primary_key=True, default='X')
    
    # Based on the Signleton design pattern. Overwrites the primary key, so there won't
    # be an entry if one exists already leaving only one entry in the table
    def save(self, *args, **kwargs):
        self.pk = 'X'
        try:
            super().save(*args, **kwargs)
        except IntegrityError:  
            """
            Because this table was built using the Singleton design pattern, If an attempt is made to make an entry, it will always result to the same pk, leading to the IntegrityError.
            Hence catch the error and make an overwrite instead.
            Typically, the update_or_create method should be used. This method override was created to protect against anyone who choose to use the save method
            """
            existing_instance = EntryTracker.objects.get(pk=self.pk)
            existing_instance.item_id = self.item_id
            existing_instance.save()
    
class BaseItem(models.Model):
    item_id = models.IntegerField(unique=True)
    deleted = models.BooleanField(default=False)
    by = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    entry_time = models.DateTimeField(default=timezone.now)
    dead = models.BooleanField(default=False)
    kids = models.JSONField(null=True, blank=True)
    hash = models.CharField(max_length=64)

    class Meta:
        abstract = True  # This makes BaseItem an abstract base class
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError: # In the odd case that item_id clashes, return False
            return False
    
class HackerNewsStory(BaseItem):
    TYPE = 'story'
    SOURCE = 'hns'
    
    url = models.URLField(null=True, blank=True)
    descendants = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

class HackerNewsJob(BaseItem):
    TYPE = 'job'
    SOURCE = 'hns'

    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

class HackerNewsComment(BaseItem):
    TYPE = 'comment'
    SOURCE = 'hns'

    text = models.TextField(null=True, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    
class HackerNewsPoll(BaseItem):
    TYPE = 'poll'
    SOURCE = 'hns'


    parts = models.JSONField(null=True, blank=True)
    descendants = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
class HackerNewsPollOption(BaseItem):    
    TYPE = 'pollopt'
    SOURCE = 'hns'

    parent = models.IntegerField(null=True, blank=True)
    
class CodeWaveStory(BaseItem):    
    TYPE = 'story'
    SOURCE = 'cwe'

    url = models.URLField(null=True, blank=True)
    descendants = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

class CodeWaveJob(BaseItem):    
    TYPE = 'job'
    SOURCE = 'cwe'

    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

class CodeWaveComment(BaseItem):    
    TYPE = 'comment'
    SOURCE = 'cwe'

    text = models.TextField(null=True, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    
class CodeWavePoll(BaseItem):    
    TYPE = 'poll'
    SOURCE = 'cwe'

    parts = models.JSONField(null=True, blank=True)
    descendants = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
class CodeWavePollOption(BaseItem):    
    TYPE = 'pollopt'
    SOURCE = 'cwe'

    poll = models.IntegerField(default=0)
    text = models.TextField(default='')
    
    