# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    # Obtener los posts de la API externa
    response = requests.get(settings.API_URL)
    posts = response.json()

    # Número total de respuestas (posts)
    total_responses = len(posts)

    # Número total de usuarios únicos
    total_users = len(set(post['userId'] for post in posts))

    # Longitud promedio de títulos
    avg_title_length = sum(len(post['title']) for post in posts) / total_responses

    # ID máximo de post (último creado en jsonplaceholder)
    max_post_id = max(post['id'] for post in posts)

    # --------- INDICADORES PERSONALIZADOS ----------
    indicator_2 = total_users
    indicator_3 = round(avg_title_length, 2)
    indicator_4 = max_post_id

    # --------- GRÁFICO: Cantidad de posts por usuario ---------
    posts_per_user = {}
    for post in posts:
        uid = post['userId']
        posts_per_user[uid] = posts_per_user.get(uid, 0) + 1

    chart_labels = list(posts_per_user.keys())   # IDs de usuario
    chart_values = list(posts_per_user.values()) # Nº de posts por usuario

    context = {
        'title': "Dashboard de JSON Placeholder",
        'total_responses': total_responses,
        'indicator_2': indicator_2,
        'indicator_3': indicator_3,
        'indicator_4': indicator_4,
        'posts': posts[:10],       # mostramos solo 10 en la tabla
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }

    return render(request, 'dashboard/index.html', context)
