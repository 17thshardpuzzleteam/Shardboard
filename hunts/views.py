from django.shortcuts import render
from django.views.decorators.http import require_GET

from hunts.models import Puzzle, Round


@require_GET
def index(request):
    return render(request, 'index.html', {
        'puzzles': Puzzle.objects.filter(hunt__web_user_id=request.user.id).order_by('-unlock_time'),
        'rounds': Round.objects.filter(hunt__web_user_id=request.user.id)
    })
