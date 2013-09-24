import os, re, urlparse, ttag
from xml.etree import ElementTree

from django import template
from django.core.urlresolvers import reverse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.template.defaulttags import URLNode, url
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode

from ..models import Study, Group, CONDITION

register = template.Library()
    
@register.tag(name="study")
class StudyTag(ttag.Tag):
    """
    Tag will create a switch to show/hide content f student is enrolled in the given experiment.
    If the user is not in any of the study groups and then content in a tag with the alternative 'NA' will be displayed.
    
    Usage
        {% study '<study_name>' '<alternative>' %}
            study content goes here
        {% endstudy %}
        
        {% study '<study_name>' 'NA' %}
            content for people not in a study condition goes here
        {% endstudy %}

        {% study '<study_name>'  %}
            content for anyone in this study
        {% endstudy %}

        {% study '<study_name>' 'ALL' %}
            content for anyone in this study
        {% endstudy %}
        
    """
    study   = ttag.BasicArg()
    group   = ttag.BasicArg(required=False, default='"ALL"')    

    class Meta:
       block = True
       end_block = 'endstudy'

    def render(self, context):
        
        data = self.resolve(context)
        #print data
        #print "HI3"
        study_name  = _strip_quotes(data['study'])
        group_name  = _strip_quotes(data['group'])        
        
        #print "HI2"

        if context['request'].user.is_authenticated():            
            user = context['request'].user
        else:
            # if there is no user, don't print anything...
            return ''
        
        #print "HI1"
        #print study_name
        #print group_name
        #print user

        does_study_exist    = len(Study.objects.filter(name=study_name)) >= 1
        is_in_this_group    = len(Group.objects.filter(study__name=study_name, name=group_name, participants__in=[user])) >= 1
        is_in_any_condition = len(Group.objects.filter(study__name=study_name, type=CONDITION,  participants__in=[user])) >= 1
        is_na               = (group_name == "NA")
        is_for_all          = (group_name == "ALL")

        #print does_study_exist
        #print is_in_this_group
        #print is_in_any_condition
        #print is_na

        content = self.nodelist.render(context)        
        
        t = template.loader.get_template("laboratory/study.html")

        if does_study_exist:
            if is_in_any_condition:
                if is_in_this_group or is_for_all:                    
                    return t.render(Context({'study_name':study_name, 'group_name':group_name, 'content':content })) 
                elif not is_in_this_group:
                    return ''
                else:
                    return ''
            else: # user hasn't been assigned to any condition
                if is_na:
                    # show the content if meant for unassigned people
                    return t.render(Context({'study_name':study_name, 'content':content })) 
                else:
                    # don't show content if meant for user in a condition
                    return ""
        else:
            return "Laboratory error: %s does not exist" % (study_name)

        return "<p>Laboratory errror: %s %s %s  %s  %s %s</p>" % (study_name, group_name, user, is_in_this_group, is_in_any_condition, is_na)

        # if does_study_exist:
        #     if is_in_this_group :            
        #         #return content                
        #         t = template.loader.get_template("laboratory/study.html")
        #         c = Context({'study_name':study_name, 'group_name':group_name, 'content':content })
        #         return t.render(c)   
        #     elif is_in_any_condition and (group_name == "ALL"):
        #         t = template.loader.get_template("laboratory/study.html")
        #         c = Context({'study_name':study_name, 'content':content })
        #         return t.render(c)   
        #     elif is_in_any_condition:
        #         return ''       
        #     elif is_na:
        #         t = template.loader.get_template("laboratory/study.html")
        #         c = Context({'study_name':study_name, 'group_name':group_name, 'content':content })
        #         return t.render(c)    
        #     elif not is_in_this_group:                
        #         return ''
        #     else:
        #         return "<p>Laboratory errror: %s %s %s  %s  %s %s</p>" % (study_name, group_name, user, is_in_this_group, is_in_any_condition, is_na)
        # else:            
        #     return 'zoo'
        #     return ''
        
    
def _strip_quotes(arg):
    if not (arg[0] == arg[-1] and arg[0] in ('"', "'")):
        raise template.TemplateSyntaxError("Argument %s should be in quotes" % arg)
    return arg[1:-1]

