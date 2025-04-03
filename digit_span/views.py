from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.templatetags.static import static
import json
from .models import Test, PlayerCount

def home(request):
    return render(request, 'digit_span/home.html')

def index(request):
    round_number = request.GET.get('round_number')
    name = request.GET.get('name', 'Unknown')
    music_type = request.GET.get('music_type', 'None')
    both_ears = request.GET.get('both_ears', 'True')

    try:
        round_number = int(round_number)
    except (TypeError, ValueError):
        round_number = 1  # Default value if conversion fails or parameter is missing

    player_count_instance, created = PlayerCount.objects.get_or_create(id=1)
    player_count = player_count_instance.count

    if round_number == 2 or round_number == 3:
        both_ears = 'false'
    else:
        both_ears = 'true'

    if round_number == 1:
        music_type = 'Classical' if player_count % 2 == 0 else 'Rock'
        player_count_instance.increment()
    elif round_number == 5:
        music_type = 'None'
    elif music_type == 'Classical':
        music_type = 'Rock'
    elif music_type == 'Rock':
        music_type = 'Classical'
    else:
        raise ValueError("Something is wrong")
        
    music_files = {
        ('Classical', 'true'): 'digit_span/Classical.mp3',
        ('Classical', 'false'): 'digit_span/ClassicalAlternating.mp3',
        ('Rock', 'true'): 'digit_span/Rock.mp3',
        ('Rock', 'false'): 'digit_span/RockAlternating.mp3',
        ('None', 'true'): None,
        ('None', 'false'): None
    }
    audio_file = music_files.get((music_type, both_ears))

    return render(request, 'digit_span/index.html', {
        'round_number': round_number,
        'name': name,
        'music_type': music_type,
        'both_ears': both_ears,
        'audio_file': static(audio_file) if audio_file else None,
    })


@csrf_exempt  # Temporarily disable CSRF for testing (enable in production)
def submit_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON request body
            name = data.get('name')
            round = data.get('round', 0)
            music = data.get('music')
            bothEars = data.get('bothEars')
            score = data.get('score')

            if name and score is not None:  # Ensure required fields are present
                test = Test.objects.create(name=name, round=round, score=score, music=music, bothEars=bothEars)
                return JsonResponse({'message': 'Score submitted successfully!'}, status=201)
            else:
                return JsonResponse({'error': 'Missing fields'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_scores(request):
    tests = Test.objects.all().order_by('-id')  # Get all scores, highest first
    data = [{'id': p.id, 'name': p.name, 'round': p.round, 'music': p.music, 'bothEars': p.bothEars, 'score': p.score} for p in tests]
    return JsonResponse(data, safe=False)