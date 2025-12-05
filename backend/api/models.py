from django.db import models
from django.utils import timezone


class Game(models.Model):
    """
    A simple Tic Tac Toe game state model.
    Board is stored as a 9-char string using underscores '_' for empty cells.
    next_player: 'X' or 'O'
    winner: 'X' or 'O' (nullable)
    is_draw: True when the board is full and there's no winner
    """
    board = models.CharField(max_length=9, default="_________")
    next_player = models.CharField(max_length=1, default="X")
    winner = models.CharField(max_length=1, null=True, blank=True)
    is_draw = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    WIN_LINES = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __str__(self) -> str:
        return f"Game {self.pk} - next: {self.next_player}, winner: {self.winner or '-'}, draw: {self.is_draw}"

    # PUBLIC_INTERFACE
    def board_as_list(self):
        """Convert internal board string to a list of 9 values: 'X', 'O', or None."""
        return [c if c in ("X", "O") else None for c in self.board]

    # PUBLIC_INTERFACE
    def set_board_from_list(self, values):
        """Set board string from a list of 9 values: 'X', 'O', or None."""
        if not isinstance(values, (list, tuple)) or len(values) != 9:
            raise ValueError("Board must be a list/tuple of 9 items")
        normalized = []
        for v in values:
            if v in ("X", "O"):
                normalized.append(v)
            elif v is None:
                normalized.append("_")
            else:
                raise ValueError("Board values must be 'X', 'O', or None")
        self.board = "".join(normalized)

    def _detect_winner(self):
        """Return 'X' or 'O' if a winning line exists, else None."""
        b = self.board
        for a, b_ix, c in self.WIN_LINES:
            line = (b[a], b[b_ix], b[c])
            if line[0] != "_" and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def _is_board_full(self) -> bool:
        return "_" not in self.board

    # PUBLIC_INTERFACE
    def reset(self):
        """Reset the game to initial state."""
        self.board = "_________"
        self.next_player = "X"
        self.winner = None
        self.is_draw = False

    # PUBLIC_INTERFACE
    def make_move(self, index: int):
        """
        Make a move for the current next_player at the given index (0-8).
        Validates:
        - game not finished
        - index in range and empty
        Applies move, updates winner/draw and toggles next_player.
        Returns self for chaining.
        """
        if self.winner or self.is_draw:
            raise ValueError("Game is already finished")

        if not isinstance(index, int) or index < 0 or index > 8:
            raise ValueError("Index must be an integer between 0 and 8")

        if self.board[index] != "_":
            raise ValueError("Cell is already occupied")

        current = list(self.board)
        current[index] = self.next_player
        self.board = "".join(current)

        winner = self._detect_winner()
        if winner:
            self.winner = winner
            self.is_draw = False
        else:
            if self._is_board_full():
                self.is_draw = True
                self.winner = None
            else:
                # toggle player
                self.next_player = "O" if self.next_player == "X" else "X"

        # updated_at will auto update on save()
        return self
