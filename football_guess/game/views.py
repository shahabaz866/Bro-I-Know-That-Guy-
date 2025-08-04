from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache


SECRET_NAME = "MESSI"
FOOTBALLER_IMAGE = "/static/img/messi.jpg"
@never_cache
def guess_game(request):
    if 'guesses' not in request.session:
            request.session['guesses'] = []


    guesses = request.session['guesses']
    word_display = [letter if letter in guesses else '_' for letter in SECRET_NAME]
    reveal_image = all(letter in guesses for letter in set(SECRET_NAME))

    feedback = ''
    if request.method == 'POST':
        guess = request.POST.get('letter', '').upper()
        if guess and guess.isalpha():
            if guess in SECRET_NAME and guess not in guesses:
                guesses.append(guess)
                feedback = f'Correct! Revealed {guess}.'
            elif guess in guesses:
                feedback = f'You already guessed {guess}.'
            else:
                feedback = f'{guess} is incorrect.'
            request.session['guesses'] = guesses
        else:
            feedback = 'Please enter a valid letter.'

    context = {
        'word_display': word_display,
        'reveal_image': reveal_image,
        'image_url': FOOTBALLER_IMAGE,
        'feedback': feedback,
    }

    return render(request, 'game/index.html', context)