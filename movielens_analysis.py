import csv
from collections import defaultdict
from datetime import datetime
import statistics


class Ratings:
    def __init__(self, path):
        self.data = []
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['rating'] = float(row['rating'])
                row['timestamp'] = int(row['timestamp'])
                self.data.append(row)

    class Movies:
        def __init__(self, ratings, movies_path):
            self.ratings = ratings
            self.movies = {}

            with open(movies_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.movies[row['movieId']] = row['title']

        def dist_by_year(self):
            result = defaultdict(int)
            for r in self.ratings.data:
                year = datetime.fromtimestamp(r['timestamp']).year
                result[year] += 1
            return dict(sorted(result.items()))

        def dist_by_rating(self):
            result = defaultdict(int)
            for r in self.ratings.data:
                result[r['rating']] += 1
            return dict(sorted(result.items()))

        def top_by_num_of_ratings(self, n):
            count = defaultdict(int)
            for r in self.ratings.data:
                if r['movieId'] in self.movies:
                    count[r['movieId']] += 1

            sorted_movies = sorted(count.items(), key=lambda x: x[1], reverse=True)

            result = {}
            for m, c in sorted_movies:
                result[self.movies[m]] = c
                if len(result) == n:
                    break
            return result

        def top_by_ratings(self, n):
            scores = defaultdict(list)
            for r in self.ratings.data:
                if r['movieId'] in self.movies:
                    scores[r['movieId']].append(r['rating'])

            avg = {m: sum(v)/len(v) for m, v in scores.items()}
            sorted_avg = sorted(avg.items(), key=lambda x: x[1], reverse=True)

            result = {}
            for m, v in sorted_avg:
                result[self.movies[m]] = round(v, 2)
                if len(result) == n:
                    break
            return result

        def top_controversial(self, n):
            scores = defaultdict(list)
            for r in self.ratings.data:
                if r['movieId'] in self.movies:
                    scores[r['movieId']].append(r['rating'])

            var = {
                m: statistics.variance(v)
                for m, v in scores.items()
                if len(v) > 1
            }

            sorted_var = sorted(var.items(), key=lambda x: x[1], reverse=True)

            result = {}
            for m, v in sorted_var:
                result[self.movies[m]] = round(v, 2)
                if len(result) == n:
                    break
            return result


class Tags:
    def __init__(self, path):
        self.tags = []
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tags.append(row['tag'])

    def most_words(self, n):
        unique = set(self.tags)
        result = {t: len(t.split()) for t in unique}
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        unique = set(self.tags)
        return sorted(unique, key=len, reverse=True)[:n]

    def most_popular(self, n):
        count = defaultdict(int)
        for t in self.tags:
            count[t] += 1
        return dict(sorted(count.items(), key=lambda x: x[1], reverse=True)[:n])

    def tags_with(self, word):
        return sorted(set(t for t in self.tags if word.lower() in t.lower()))