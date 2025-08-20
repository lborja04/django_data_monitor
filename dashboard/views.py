# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    # Obtener los posts de la API externa
    response = requests.get(settings.API_URL)
    posts = response.json()

    # Número total de respuestas
    total_responses = len(posts)

    # Ejemplo de indicadores: podemos usar los primeros 4 posts para mostrar títulos
    # o generar datos ficticios para indicadores adicionales
    indicator_2 = len(posts[0]['body'].split()) if len(posts) > 0 else 0
    indicator_3 = len(posts[1]['body'].split()) if len(posts) > 1 else 0
    indicator_4 = len(posts[2]['body'].split()) if len(posts) > 2 else 0

    # Datos para el gráfico: número de caracteres de cada título
    chart_labels = [post['title'][:15] for post in posts[:10]]  # primeras 10 publicaciones
    chart_values = [len(post['title']) for post in posts[:10]]

    context = {
        'title': "Landing Page' Dashboard",
        'total_responses': total_responses,
        'posts': posts[:10],  # limitar a 10 para la tabla
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }

    return render(request, 'dashboard/index.html', context)
