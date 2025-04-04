from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def clean_url(request):
    query_params = request.GET.copy()

    # Убираем пустые параметры
    for key in list(query_params.keys()):
        values = [value for value in query_params.getlist(key) if value]
        if values:
            query_params.setlist(key, values)
        else:
            del query_params[key]

    # Оставляем только последний параметр "page"
    if 'page' in query_params:
        query_params.pop('page', None)  # Полностью удаляем все параметры "page"

    return '?' + urlencode(query_params, doseq=True)