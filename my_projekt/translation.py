from django import http
from django.utils.http import is_safe_url
from django.utils.translation.trans_real import check_for_language, get_language
from django.conf import settings
from django.utils import translation


def set_language(request):
    lang_code = request.GET.get('LANGUAGES', 'ru')
    lang = get_language()
    if not lang_code:
        lang_code = request.GET.get('LANGUAGE_CODE', settings.LANGUAGE_CODE)
    next_url = request.META.get('HTTP_REFERER', None)
    if not is_safe_url:
        next_url = '/'
    response = http.HttpResponseRedirect(next_url)
    if lang_code and check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        translation.activate(lang_code)
    return response
