from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import Hunt, Round, Puzzle, Tag, PuzzleTag

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


class PuzzleTagInline(admin.TabularInline):
    model = PuzzleTag
    extra = 1
    autocomplete_fields = ("tag",)

@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ("get_rounds", "name", "answer", "priority", "get_tags")
    list_display_links = ('name',)
    list_filter = ("rounds", "priority", "is_meta")
    filter_horizontal = ("rounds", "feeders")
    inlines = [PuzzleTagInline]

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

    def get_tags(self, obj):
        return ", ".join([f"{tag.marker} {tag.name}" for tag in obj.tags.all()])

    get_tags.short_description = "Tags"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("marker", "name", "role")
    search_fields = ("marker", "name", "role")

@admin.register(PuzzleTag)
class PuzzleTagAdmin(admin.ModelAdmin):
    list_display = ("puzzle", "tag", "added_at")
    list_filter = ("puzzle", "tag",)
    search_fields = ("puzzle__name", "tag__name", "tag__marker")

Hunt.__str__ = lambda self: f'{self.name}'
Round.__str__ = lambda self: f'{self.marker} {self.name}'
Puzzle.__str__ = lambda self: f'{"".join([round.marker for round in self.rounds.all()])} {self.name}'
Tag.__str__ = lambda self: f'{self.marker} {self.name}'