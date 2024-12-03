from django import forms
from .models import stickyNote, Notebook
from tinymce.widgets import TinyMCE

from .models import Task


FORM_CONTROL_CLASS = 'form-control my-3' #defining a constant (adaptability)


class stickyNotesForm(forms.ModelForm):
    class Meta:
        model=stickyNote
        fields =('title','text')
        widgets = {
            'title': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS}),
            'text':  forms.Textarea(attrs={'class': FORM_CONTROL_CLASS}),
            
        }
        labels={
            'text':'Write your thoughts'
        }

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notebook
        fields =('title','text')
        widgets = {
            'title': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS}),
            'text': TinyMCE(attrs={'class': FORM_CONTROL_CLASS, 'cols': 80, 'rows': 30}), 
            
        }
        labels={
            'text':'Write your thoughts'
        }



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'task-input',
                'placeholder': 'Add a new task'
            }),
        }