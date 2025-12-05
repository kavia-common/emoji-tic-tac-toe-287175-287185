from rest_framework import serializers
from .models import Game


class BoardField(serializers.Field):
    """
    Custom field exposing the board as an array of 9 values: 'X', 'O', or None.
    """

    def to_representation(self, value: str):
        # value is the model field string like "X_O____OX"
        return [c if c in ("X", "O") else None for c in value]

    def to_internal_value(self, data):
        # We generally do not accept direct set through serializer; keep for completeness
        if not isinstance(data, (list, tuple)) or len(data) != 9:
            raise serializers.ValidationError("Board must be a list of 9 items")
        result = []
        for v in data:
            if v in ("X", "O"):
                result.append(v)
            elif v is None:
                result.append("_")
            else:
                raise serializers.ValidationError("Board values must be 'X', 'O', or None")
        return "".join(result)


class GameSerializer(serializers.ModelSerializer):
    board = BoardField(read_only=True)

    class Meta:
        model = Game
        fields = ["id", "board", "next_player", "winner", "is_draw", "created_at", "updated_at"]
        read_only_fields = ["id", "board", "next_player", "winner", "is_draw", "created_at", "updated_at"]
