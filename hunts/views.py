from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from hunts.forms import AddPuzzleForm
from hunts.messaging import discord_interface
from hunts.models import Puzzle, Round


@require_GET
def index(request):
    puzzles = Puzzle.objects.filter(hunt__web_user_id=request.user.id)
    puzzle_sets = []
    for meta in puzzles.filter(is_meta=True).order_by('-unlock_time'):
        puzzle_sets.append({
            'meta': meta,
            'puzzles': meta.feeders.order_by('-unlock_time')
        })
    puzzle_sets.append({
        'meta': None,
        'puzzles': puzzles.filter(feeding__isnull=True, is_meta=False)
    })
    return render(request, 'index.html', {
        'puzzle_sets': puzzle_sets,
        'rounds': Round.objects.filter(hunt__web_user_id=request.user.id),
        'add_puzzle_form': AddPuzzleForm(request.user.id)
    })


@require_POST
def add_round(request):
    data = request.POST.dict()
    discord_interface.send_message('!round ' + data['name'] + ' -marker=' + data['marker'])
    return HttpResponseRedirect('/')


@require_POST
def add_puzzle(request):
    data = request.POST.dict()
    discord_interface.send_message('!create ' + data['name'] + ' -round=' + Round.objects.filter(id=data['rounds']).first().name)
    return HttpResponseRedirect('/')
