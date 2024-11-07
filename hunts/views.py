from django.shortcuts import render
from django.views.decorators.http import require_GET

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
        'rounds': Round.objects.filter(hunt__web_user_id=request.user.id)
    })
