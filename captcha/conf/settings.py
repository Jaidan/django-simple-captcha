import os
from django.conf import settings

CAPTCHA_FONT_PATH = getattr(settings,'CAPTCHA_FONT_PATH', os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'fonts/etl24-unicode.pil'))) 
CAPTCHA_FONT_SIZE = getattr(settings,'CAPTCHA_FONT_SIZE', 22)
CAPTCHA_BACKGROUND_COLOR = getattr(settings,'CAPTCHA_BACKGROUND_COLOR', '#ffffff')
CAPTCHA_FOREGROUND_COLOR= getattr(settings,'CAPTCHA_FOREGROUND_COLOR', '#001100')
CAPTCHA_CHALLENGE_FUNCT = getattr(settings,'CAPTCHA_CHALLENGE_FUNCT','captcha.helpers.random_char_challenge')
CAPTCHA_NOISE_FUNCTIONS = getattr(settings,'CAPTCHA_NOISE_FUNCTIONS', ('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',))
CAPTCHA_FILTER_FUNCTIONS = getattr(settings,'CAPTCHA_FILTER_FUNCTIONS',('captcha.helpers.post_smooth',))
CAPTCHA_WORDS_DICTIONARY = getattr(settings,'CAPTCHA_WORDS_DICTIONARY', '/usr/share/dict/words')
CAPTCHA_FLITE_PATH = getattr(settings,'CAPTCHA_FLITE_PATH',None)
