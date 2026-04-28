from movielens_analysis import Ratings, Tags


def test_ratings_load():
    r = Ratings("data/ratings_small.csv")
    assert isinstance(r.data, list)


def test_tags():
    t = Tags("data/tags_small.csv")
    res = t.longest(5)
    assert isinstance(res, list)
