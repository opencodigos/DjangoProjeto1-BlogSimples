from django import forms
from .models import Posts

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'