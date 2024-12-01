from datetime import datetime, timedelta
from typing import List, Generator


class Movie:
    def __init__(self, name: str, schedule: List = None):
        self._name = name
        self._movie_schedule = schedule

    @property
    def name(self):
        return self._name

    def schedule(self) -> Generator:
        """create generator for getting days of movie"""
        for start, finish in self._movie_schedule:
            yield from (
                start + timedelta(days=i) for i in range((finish - start).days + 1)
            )  # +1 for include right border
