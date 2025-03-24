from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Имя")
    email = forms.EmailField()
    to = forms.EmailField(label="Кому(email)")
    comment = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )
