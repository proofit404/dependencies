from django import forms


class QuestionForm(forms.Form):

    question_text = forms.CharField(widget=forms.Textarea)
    pub_date = forms.DateTimeField()
