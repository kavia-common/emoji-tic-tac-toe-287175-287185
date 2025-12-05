from django.urls import path
from .views import (
    health,
    create_game,
    retrieve_game,
    make_move,
    reset_game,
)

urlpatterns = [
    path('health/', health, name='Health'),

    # Game endpoints
    path('games/', create_game, name='CreateGame'),               # POST /api/games/
    path('games/<int:pk>/', retrieve_game, name='RetrieveGame'),  # GET /api/games/{id}/
    path('games/<int:pk>/move/', make_move, name='MakeMove'),     # POST /api/games/{id}/move/
    path('games/<int:pk>/reset/', reset_game, name='ResetGame'),  # POST /api/games/{id}/reset/
]
