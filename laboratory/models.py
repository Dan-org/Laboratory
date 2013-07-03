from datetime import datetime
from django.db import models
from django.conf import settings

# See https://github.com/mixcloud/django-experiments for another approaach
# https://github.com/disqus/gargoyle

# Study groups can be of several types depending on the participants current status.
UNASSIGNED  = 'unassigned'
DROPPED     = 'dropped'
CONDITION   = 'condition'
GROUP_TYPES = [
    (UNASSIGNED,  'Unassigned'),
    (DROPPED,     'Dropped'),
    (CONDITION,   'Condition'),
]

class Study(models.Model):
    """
    Study represents an experiment or observational study.
    """
    name        = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    end_date    = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_conditions():
        pass
    
    class Meta:
        verbose_name_plural = "studies"

   
class Group(models.Model):
    """
    Group specifies a group of participants in a study -- the group can be the whole pool, those
    assigned to a specific condition, control group, dropped, unassigned etc.
    """
    name            = models.CharField(max_length=255)
    study           = models.ForeignKey(Study, related_name="groups")
    participants    = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)
    description     = models.TextField(null=True, blank=True)
    type            = models.SlugField(choices=GROUP_TYPES, default=CONDITION)
    
    def __unicode__(self):
        return "%s %s" % (self.study.name, self.name)
    
    
class LabPage(models.Model):
    """
    Wrapper for discourse document used to present page
    """
    name        = models.CharField(max_length=255)
    title       = models.CharField(max_length=255, null=True, blank=True)
    slug        = models.SlugField()
    # don't think this is necessary
    #study       = models.ForeignKey(Study, related_name="pages") 
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)

    