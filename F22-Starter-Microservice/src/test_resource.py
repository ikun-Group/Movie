import json
from movie_resource import MovieResource


def t1():
    res = MovieResource.get_by_template(['*'], {'guid': '11cad065-1be5-4508-84d3-6d1e8efa30f9'})
    print(json.dumps(res, indent=2, default=str))


def t2():
    res = MovieResource.create_movie('Avatar', 'sci-fi', 2022, 7.8)
    print(json.dumps(res, indent=2, default=str))


def t3():
    res = MovieResource.delete_movie('fceeec6a-4830-4a09-9b9e-85ef2df69314')


if __name__ == "__main__":
    t1()
