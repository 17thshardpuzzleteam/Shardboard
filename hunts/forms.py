from django import forms
from django.db.models.query import EmptyQuerySet

from hunts.models import Round, Puzzle


class AddRoundForm(forms.Form):
    name = forms.CharField(label="Name", max_length=255, required=True)
    marker = forms.CharField(label="Marker", max_length=7, required=True)

    def __init__(self, user_id):
        super().__init__()


class AddPuzzleForm(forms.Form):
    name = forms.CharField(label="Name", max_length=511, required=True)
    is_meta = forms.BooleanField(label='Is Meta?', required=False)
    rounds = None
    feeders = None

    def __init__(self, user_id):
        super().__init__()
        self.fields['rounds'] = forms.ModelChoiceField(label='Round', queryset=Round.objects.filter(hunt__web_user_id=user_id).order_by('-id'), required=True)
        self.fields['feeders'] = forms.ModelMultipleChoiceField(label='Feeders', queryset=Puzzle.objects.filter(hunt__web_user_id=user_id).order_by('name'), required=False)


class SolvePuzzleForm(forms.Form):
    answer = forms.CharField(label="Answer", max_length=255, required=True)

    def __init__(self, user_id):
        super().__init__()
