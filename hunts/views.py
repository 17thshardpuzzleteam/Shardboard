from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from hunts.forms import AddRoundForm, AddPuzzleForm
from hunts.models import Puzzle, Round, Hunt
from datetime import datetime


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
        'add_round_form': AddRoundForm(request.user.id),
        'add_puzzle_form': AddPuzzleForm(request.user.id)
    })


@require_POST
def add_round(request):
    data = request.POST.dict()
    # discord_interface.send_message('!round ' + data['name'] + ' -marker=' + data['marker'])
    # todo make this in db
    return HttpResponseRedirect('/')


@require_POST
def add_puzzle(request):
    # todo rejection checking: reject existing name, etc
    data = request.POST.dict()
    hunt = Hunt.objects.get(web_user_id=request.user.id)
    pending_puzzles = Puzzle.objects.filter(channel_id__lt=0, hunt_id=hunt.id)
    new_puzzle = Puzzle.objects.create(name=data['name'], channel_id=-(len(pending_puzzles) + 1), hunt_id=hunt.id,
                                       spreadsheet_link='', unlock_time=datetime.now(), priority='New')
    new_puzzle.rounds.add(Round.objects.filter(id=data['rounds']).first())
    return HttpResponseRedirect('/')
