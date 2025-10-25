from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from hunts.forms import AddRoundForm, AddPuzzleForm, SolvePuzzleForm
from hunts.models import Puzzle, Round, Hunt, Tag, PuzzleTag
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
        'add_puzzle_form': AddPuzzleForm(request.user.id),
        'solve_puzzle_form': SolvePuzzleForm(request.user.id),
        'all_tags': Tag.objects.all().order_by('name'),
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
    # channel id doesn't actually matter here, we just want it to be unique per-hunt
    new_puzzle = Puzzle.objects.create(name=data['name'], channel_id=-(len(pending_puzzles) + 1), hunt_id=hunt.id,
                                       spreadsheet_link='', unlock_time=datetime.now(), priority='New', update_flag=True)
    new_puzzle.rounds.add(Round.objects.filter(id=data['rounds']).first())
    return HttpResponseRedirect('/')


@require_POST
def solve_puzzle(request):
    data = request.POST.dict()
    Puzzle.objects.filter(id=data['id']).update(answer=data['answer'].upper(), priority='Solved',
                                             solve_time=datetime.now(), update_flag=True)

    return HttpResponseRedirect('/')


@require_POST
def add_tag(request):
    data = request.POST.dict()
    puzzle_id = data.get("puzzle_id")
    tag_id = data.get("tag_id")

    if not puzzle_id or not tag_id:
        return HttpResponseRedirect('/')

    puzzle = get_object_or_404(Puzzle, id=puzzle_id)
    tag = get_object_or_404(Tag, id=tag_id)

    PuzzleTag.objects.get_or_create(puzzle=puzzle, tag=tag)

    Puzzle.objects.filter(id=puzzle.id).update(update_flag=True)

    return HttpResponseRedirect('/')


@require_POST
def remove_tag(request):
    data = request.POST.dict()
    puzzle_id = data.get("puzzle_id")
    tag_id = data.get("tag_id")

    if not puzzle_id or not tag_id:
        return HttpResponseRedirect('/')

    puzzle = get_object_or_404(
        Puzzle,
        id=puzzle_id
    )

    PuzzleTag.objects.filter(
        puzzle_id=puzzle.id,
        tag_id=tag_id,
    ).delete()

    Puzzle.objects.filter(id=puzzle.id).update(update_flag=True)

    return HttpResponseRedirect('/')