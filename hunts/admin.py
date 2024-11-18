from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import Hunt, Round, Puzzle

@admin.register(Hunt)
class HuntAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput()},
    }

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("marker", "name", "hunt")
    list_display_links = ('name',)

    formfield_overrides = {
        models.IntegerField: {'widget': TextInput()},
    }

@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ("get_rounds", "name", "answer", "priority")
    list_display_links = ('name',)
    list_filter = ("rounds", "priority", "is_meta")
    filter_horizontal = ("rounds", "feeders")

    formfield_overrides = {
        models.IntegerField: {'widget': TextInput()},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(PuzzleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['answer'].required = False
        form.base_fields['notes'].required = False
        form.base_fields['solve_time'].required = False
        form.base_fields['feeders'].required = False
        return form

    def get_rounds(self, obj):
        return "".join([round.marker for round in obj.rounds.all()])
    
    get_rounds.short_description = 'Round'

Hunt.__str__ = lambda self: f'{self.name}'
Round.__str__ = lambda self: f'{self.marker} {self.name}'
Puzzle.__str__ = lambda self: f'{"".join([round.marker for round in self.rounds.all()])} {self.name}'