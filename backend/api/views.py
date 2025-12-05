from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Game
from .serializers import GameSerializer


@api_view(['GET'])
def health(request):
    """Simple health endpoint to verify server is running."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="create_game",
    operation_summary="Create a new Tic Tac Toe game",
    operation_description="Creates and returns a fresh game with empty board, next_player='X'.",
    responses={201: GameSerializer},
    tags=["games"],
)
@api_view(["POST"])
def create_game(request):
    """
    Create and return a new Tic Tac Toe game.

    Response:
      201 Created with Game payload
    """
    game = Game.objects.create()
    serializer = GameSerializer(game)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_id="retrieve_game",
    operation_summary="Retrieve a game",
    operation_description="Retrieve a game by its id.",
    responses={200: GameSerializer, 404: "Not Found"},
    tags=["games"],
)
@api_view(["GET"])
def retrieve_game(request, pk: int):
    """
    Retrieve a game by id.

    Path params:
      pk: integer id of the Game

    Response:
      200 OK with Game payload
      404 if not found
    """
    game = get_object_or_404(Game, pk=pk)
    serializer = GameSerializer(game)
    return Response(serializer.data)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="make_move",
    operation_summary="Make a move",
    operation_description="Make a move at the provided index (0-8) for the current next_player.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["index"],
        properties={
            "index": openapi.Schema(type=openapi.TYPE_INTEGER, description="Position index 0-8"),
        },
    ),
    responses={200: GameSerializer, 400: "Validation error", 404: "Not Found"},
    tags=["games"],
)
@api_view(["POST"])
def make_move(request, pk: int):
    """
    Make a move in the game.

    Path params:
      pk: integer id of the Game

    Body:
      {
        "index": <int 0-8>
      }

    Responses:
      200 OK with updated Game payload
      400 on validation error (e.g., out of turn, invalid index, occupied cell, finished game)
      404 if not found
    """
    game = get_object_or_404(Game, pk=pk)
    index = request.data.get("index", None)
    try:
        game.make_move(int(index))
        game.save()
        serializer = GameSerializer(game)
        return Response(serializer.data)
    except (ValueError, TypeError) as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_id="reset_game",
    operation_summary="Reset a game",
    operation_description="Reset the game to its initial state (empty board, X to play).",
    responses={200: GameSerializer, 404: "Not Found"},
    tags=["games"],
)
@api_view(["POST"])
def reset_game(request, pk: int):
    """
    Reset the specified game to its initial state.

    Responses:
      200 OK with reset Game payload
      404 if not found
    """
    game = get_object_or_404(Game, pk=pk)
    game.reset()
    game.save()
    serializer = GameSerializer(game)
    return Response(serializer.data)
