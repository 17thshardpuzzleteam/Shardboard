from django.shortcuts import render
from django.views.decorators.http import require_GET

from hunts.models import Hunt


@require_GET
def index(request):
    return render(request, 'index.html', {
        'hunts': Hunt.objects.all()
    })
