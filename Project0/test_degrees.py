import os
import unittest
from unittest.mock import patch

import degrees

SMALL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "small")

# Person ids from small/people.csv
KEVIN_BACON = "102"
TOM_CRUISE = "129"
CARY_ELWES = "144"
TOM_HANKS = "158"
DUSTIN_HOFFMAN = "163"
CHRIS_SARANDON = "1697"
VALERIA_GOLINO = "420"
EMMA_WATSON = "914612"


def assert_valid_path(test, source, target, path):
    """
    Checks that every step of the path is a real co-star link,
    starting at source and ending at target.
    """
    current = source
    for movie_id, person_id in path:
        test.assertIn(movie_id, degrees.people[current]["movies"])
        test.assertIn(person_id, degrees.movies[movie_id]["stars"])
        current = person_id
    test.assertEqual(current, target)


class TestSmallDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        degrees.names.clear()
        degrees.people.clear()
        degrees.movies.clear()
        degrees.load_data(SMALL)

    def check(self, source, target, expected_degrees):
        path = degrees.shortest_path(source, target)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), expected_degrees)
        assert_valid_path(self, source, target, path)

    def test_same_person(self):
        self.assertEqual(degrees.shortest_path(TOM_CRUISE, TOM_CRUISE), [])

    def test_one_degree(self):
        self.check(KEVIN_BACON, TOM_HANKS, 1)
        path = degrees.shortest_path(KEVIN_BACON, TOM_HANKS)
        self.assertEqual(path, [("112384", TOM_HANKS)])  # Apollo 13

    def test_two_degrees(self):
        self.check(TOM_CRUISE, TOM_HANKS, 2)

    def test_three_degrees(self):
        self.check(DUSTIN_HOFFMAN, TOM_HANKS, 3)
        self.check(CARY_ELWES, KEVIN_BACON, 3)

    def test_five_degrees(self):
        self.check(VALERIA_GOLINO, CHRIS_SARANDON, 5)

    def test_symmetric(self):
        forward = degrees.shortest_path(VALERIA_GOLINO, CHRIS_SARANDON)
        backward = degrees.shortest_path(CHRIS_SARANDON, VALERIA_GOLINO)
        self.assertEqual(len(forward), len(backward))

    def test_all_pairs_are_shortest(self):
        """
        Compares every pair of people against a distance computed
        independently by flooding outward from the source one layer at a time.
        """
        for source in degrees.people:
            distance = {source: 0}
            layer = {source}
            while layer:
                next_layer = set()
                for person in layer:
                    for _, neighbor in degrees.neighbors_for_person(person):
                        if neighbor not in distance:
                            distance[neighbor] = distance[person] + 1
                            next_layer.add(neighbor)
                layer = next_layer

            for target in degrees.people:
                with self.subTest(source=source, target=target):
                    path = degrees.shortest_path(source, target)
                    if target not in distance:
                        self.assertIsNone(path)
                    else:
                        self.assertEqual(len(path), distance[target])
                        assert_valid_path(self, source, target, path)

    def test_not_connected(self):
        self.assertIsNone(degrees.shortest_path(KEVIN_BACON, EMMA_WATSON))
        self.assertIsNone(degrees.shortest_path(EMMA_WATSON, KEVIN_BACON))


class TestHandBuiltGraph(unittest.TestCase):
    """
    A-B-C-D-E is a chain, but A and E also share a movie directly.
    A long dead-end branch hangs off B so that a search going deep
    instead of wide wanders off before finding the short route.
    """

    PEOPLE = {
        p: {"name": p, "birth": "", "movies": set()}
        for p in ["A", "B", "C", "D", "E"]
    }
    MOVIES = {
        "m1": {"title": "m1", "year": "", "stars": {"A", "B"}},
        "m2": {"title": "m2", "year": "", "stars": {"B", "C"}},
        "m3": {"title": "m3", "year": "", "stars": {"C", "D"}},
        "m4": {"title": "m4", "year": "", "stars": {"D", "E"}},
        "shortcut": {"title": "shortcut", "year": "", "stars": {"A", "E"}},
    }
    # Dead-end branch B-X1-X2-...-X8-D gives a long alternative route to D
    BRANCH = ["B"] + [f"X{i}" for i in range(1, 9)] + ["D"]
    for i in range(len(BRANCH) - 1):
        MOVIES[f"x{i}"] = {
            "title": f"x{i}", "year": "",
            "stars": {BRANCH[i], BRANCH[i + 1]},
        }
    for p in BRANCH:
        PEOPLE.setdefault(p, {"name": p, "birth": "", "movies": set()})

    def setUp(self):
        people = {p: dict(info, movies=set()) for p, info in self.PEOPLE.items()}
        for movie_id, movie in self.MOVIES.items():
            for person_id in movie["stars"]:
                people[person_id]["movies"].add(movie_id)

        patchers = [
            patch.dict(degrees.people, people, clear=True),
            patch.dict(degrees.movies, self.MOVIES, clear=True),
        ]
        for p in patchers:
            p.start()
            self.addCleanup(p.stop)

    def test_takes_shortcut(self):
        self.assertEqual(degrees.shortest_path("A", "E"), [("shortcut", "E")])

    def test_two_steps_via_shortcut(self):
        path = degrees.shortest_path("B", "E")
        self.assertEqual(len(path), 2)
        assert_valid_path(self, "B", "E", path)

    def test_every_pair_from_b(self):
        # B is 1 from A and C, 2 from D (via C) and E (via A)
        expected = {"A": 1, "C": 1, "D": 2, "E": 2, "X1": 1, "X8": 3}
        for target, n in expected.items():
            with self.subTest(target=target):
                path = degrees.shortest_path("B", target)
                self.assertEqual(len(path), n)
                assert_valid_path(self, "B", target, path)

    def test_isolated_person(self):
        degrees.people["F"] = {"name": "F", "birth": "", "movies": set()}
        self.assertIsNone(degrees.shortest_path("A", "F"))
        self.assertIsNone(degrees.shortest_path("F", "A"))


if __name__ == "__main__":
    unittest.main()
