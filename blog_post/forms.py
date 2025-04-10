from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Имя")
    email = forms.EmailField()
    to = forms.EmailField(label="Кому(email)")
    comment = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")

class SearchForm(forms.Form):
    search = forms.CharField(label="Поиск")