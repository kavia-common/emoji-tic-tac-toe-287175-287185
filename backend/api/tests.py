from rest_framework.test import APITestCase
from django.urls import reverse


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class GameApiTests(APITestCase):
    def setUp(self):
        # URL names are defined in backend/api/urls.py
        self.create_url = reverse("CreateGame")
        self.health_url = reverse("Health")

    def test_create_and_retrieve_game(self):
        # Create game
        resp = self.client.post(self.create_url, data={}, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("id", resp.data)
        game_id = resp.data["id"]

        # Assert initial payload shape
        self.assertEqual(resp.data["board"], [None] * 9)
        self.assertEqual(resp.data["next_player"], "X")
        self.assertIsNone(resp.data["winner"])
        self.assertFalse(resp.data["is_draw"])

        # Retrieve game
        retrieve_url = reverse("RetrieveGame", kwargs={"pk": game_id})
        get_resp = self.client.get(retrieve_url)
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.data["id"], game_id)
        self.assertEqual(get_resp.data["board"], [None] * 9)

    def test_valid_move_and_turn_flips(self):
        # Create game
        resp = self.client.post(self.create_url, data={}, format="json")
        self.assertEqual(resp.status_code, 201)
        game_id = resp.data["id"]

        # X plays at 0
        move_url = reverse("MakeMove", kwargs={"pk": game_id})
        m1 = self.client.post(move_url, data={"index": 0}, format="json")
        self.assertEqual(m1.status_code, 200)
        self.assertEqual(m1.data["next_player"], "O")
        board = m1.data["board"]
        self.assertEqual(board[0], "X")
        self.assertTrue(all((cell is None) for i, cell in enumerate(board) if i != 0))

        # O plays at 4
        m2 = self.client.post(move_url, data={"index": 4}, format="json")
        self.assertEqual(m2.status_code, 200)
        self.assertEqual(m2.data["next_player"], "X")
        board = m2.data["board"]
        self.assertEqual(board[0], "X")
        self.assertEqual(board[4], "O")

    def test_invalid_move_on_occupied_cell(self):
        # Create game
        resp = self.client.post(self.create_url, data={}, format="json")
        self.assertEqual(resp.status_code, 201)
        game_id = resp.data["id"]
        move_url = reverse("MakeMove", kwargs={"pk": game_id})

        # X plays at 0 (valid)
        m1 = self.client.post(move_url, data={"index": 0}, format="json")
        self.assertEqual(m1.status_code, 200)

        # O tries to play at 0 again (invalid - occupied)
        m2 = self.client.post(move_url, data={"index": 0}, format="json")
        self.assertEqual(m2.status_code, 400)
        self.assertIn("detail", m2.data)
        self.assertIn("occupied", m2.data["detail"].lower())

    def test_win_detection_blocks_further_moves(self):
        # Create game
        resp = self.client.post(self.create_url, data={}, format="json")
        self.assertEqual(resp.status_code, 201)
        game_id = resp.data["id"]
        move_url = reverse("MakeMove", kwargs={"pk": game_id})

        # Sequence to let X win on top row: X:0, O:3, X:1, O:4, X:2
        self.assertEqual(self.client.post(move_url, data={"index": 0}, format="json").status_code, 200)  # X
        self.assertEqual(self.client.post(move_url, data={"index": 3}, format="json").status_code, 200)  # O
        self.assertEqual(self.client.post(move_url, data={"index": 1}, format="json").status_code, 200)  # X
        self.assertEqual(self.client.post(move_url, data={"index": 4}, format="json").status_code, 200)  # O
        final_move = self.client.post(move_url, data={"index": 2}, format="json")  # X wins
        self.assertEqual(final_move.status_code, 200)
        self.assertEqual(final_move.data["winner"], "X")
        self.assertFalse(final_move.data["is_draw"])

        # Next move should be blocked with 400 because game is finished
        blocked = self.client.post(move_url, data={"index": 5}, format="json")
        self.assertEqual(blocked.status_code, 400)
        self.assertIn("finished", blocked.data.get("detail", "").lower())

    def test_draw_detection_blocks_further_moves(self):
        # Create game
        resp = self.client.post(self.create_url, data={}, format="json")
        self.assertEqual(resp.status_code, 201)
        game_id = resp.data["id"]
        move_url = reverse("MakeMove", kwargs={"pk": game_id})

        # Play to a draw (no three-in-a-row):
        # Indices sequence: 0:X,1:O,2:X,4:O,3:X,5:O,7:X,6:O,8:X
        sequence = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        last_resp = None
        for idx in sequence:
            last_resp = self.client.post(move_url, data={"index": idx}, format="json")
            self.assertEqual(last_resp.status_code, 200)

        # After the final move, it should be a draw
        self.assertIsNone(last_resp.data["winner"])
        self.assertTrue(last_resp.data["is_draw"])

        # Further move attempts must be blocked
        blocked = self.client.post(move_url, data={"index": 0}, format="json")
        self.assertEqual(blocked.status_code, 400)
        self.assertIn("finished", blocked.data.get("detail", "").lower())
