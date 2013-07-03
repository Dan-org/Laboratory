from django import forms
from django.conf import settings
from django.contrib import auth
from django.forms import Form

from laboratory.models import Study, Group


class EasyForm(object):
    """
    An easier way of doing forms so that they take requests instead of blank data.  Also handles
    creating the message, and can be extended later to do other things like trigger signals.
    """
    methods = ['post', 'put']

    def __init__(self, request, data = None, instance=None, msg="Form submitted.", methods=None):
        self.methods = methods or self.__class__.methods
        self.request = request
        self.msg = msg
        self.initial = dict(tup for tup in request.GET.items())
        
        kwargs = {'initial': self.initial}
        if instance is not None:
            kwargs.update({'instance': instance})

        if request.method.lower() in self.methods:
            super(EasyForm, self).__init__(data or request.POST, request.FILES, **kwargs)
        else:
            super(EasyForm, self).__init__(**kwargs)

    def is_valid(self):
        if self.request.method.lower() not in self.methods:
            return False
        return super(EasyForm, self).is_valid()

    def save(self):
        instance = super(EasyForm, self).save()
        if not self.request.is_ajax():
            messages.add_message(self.request, messages.INFO, self.msg)
        return instance
    
    
class ParticipantsForm(EasyForm, Form):
    ''' Use this form to add anonymous users to a particular condition of a study. '''
    def __init__(self, *args, **kwargs):
        self.study = kwargs.pop('study')
        #self.group = kwargs.pop('group')
        super(ParticipantsForm, self).__init__(*args, **kwargs)
        self.build()
    
    def build(self):
        self.fields['amount']   = forms.IntegerField(initial=0, min_value=1, max_value=100, widget=forms.TextInput(attrs={'size':'3'}))
        self.fields['group']    = forms.ChoiceField(choices=self.get_groups())
    
    def get_groups(self, ):
        choices = []
        for group in self.study.groups.all():
            choices.append((group.name, group))
        return choices
        
    def save(self):
        amount = int(self.cleaned_data['amount'])
        group  = Group.objects.get(name=self.cleaned_data['group'], study=self.study)
        print("SAVING... %s %s" % (amount, group.name))
        self.create_new_participants_for_group(amount, group)        
        
    def create_new_participants_for_group(self, amount, group):
        ''' Creates the given number of new participants and adds them to the given group '''
        for i in range(amount):
            try:
                p = auth.get_user_model().objects.create_participant() # we assume user model manager has defined this method
            except:
                raise Exception("User manager has not defined create_participant method")
            group.participants.add(p)
