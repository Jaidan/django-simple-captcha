from cStringIO import StringIO
from captcha.models import CaptchaStore
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import Image,ImageDraw,ImageFont,ImageFilter,random
from captcha.conf import settings

def captcha_image(request,key):
    
    store = get_object_or_404(CaptchaStore,hashkey=key)
    text=store.challenge
    tmpimage = Image.new('RGB', (10,10), settings.CAPTCHA_BACKGROUND_COLOR)
    if settings.CAPTCHA_FONT_PATH.lower().strip().endswith('ttf'):
        font = ImageFont.truetype(settings.CAPTCHA_FONT_PATH,settings.CAPTCHA_FONT_SIZE)
    else:
        font = ImageFont.load(settings.CAPTCHA_FONT_PATH)
    tmpdraw = ImageDraw.Draw(tmpimage)
    size = tmpdraw.textsize(text, font=font)
    image = tmpimage.resize((size[0]+4,size[1]+4))
    del(tmpimage,tmpdraw)
    
    draw = ImageDraw.Draw(image)
    draw.text((2, 2), text, font = font, fill = settings.CAPTCHA_FOREGROUND_COLOR)
    
    for f in settings.noise_functions():
        draw = f(draw,image)
    for f in settings.filter_functions():
        image = f(image)
    
    out = StringIO()
    image.save(out,"PNG")
    out.seek(0)
    
    response = HttpResponse()
    response['Content-Type'] = 'image/png'
    response.write(out.read())
    
    return response

def captcha_audio(request,key):
    if settings.CAPTCHA_FLITE_PATH:
        store = get_object_or_404(CaptchaStore,hashkey=key)
        text=store.challenge
        if 'captcha.helpers.math_challenge' == settings.CAPTCHA_CHALLENGE_FUNCT:
            text = text.replace('*','times').replace('-','minus')
        elif 'captcha.helpers.random_char_challenge' == settings.CAPTCHA_CHALLENGE_FUNCT:
            text = '.'.join(list(text))
            
        import tempfile, os
    
        path = str(os.path.join(tempfile.gettempdir(),'%s.wav' %key))
        cline = '%s -t "%s" -o "%s"' %(settings.CAPTCHA_FLITE_PATH, text, path)
    
        os.popen(cline).read()
        if os.path.isfile(path):
            response = HttpResponse()
            f = open(path,'rb')
            response['Content-Type'] = 'audio/x-wav'
            response.write(f.read())
            f.close()
            os.unlink(path)
            return response
    
    raise Http404
