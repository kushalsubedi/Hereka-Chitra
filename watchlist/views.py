import json 
from django.http import HttpResponse
import requests
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
api_key = settings.API_KEY

def get_movies(pages):
    api_url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={pages}'
    r = requests.get(api_url)
    data = r.json()
    return data 



def list_movies(request, page=1):
    pages = request.GET.get('page', 1)
    data = get_movies(pages)
    movies = data['results']
    print(movies[0]['title']) 
 
    ''' 
{'adult': False, 'backdrop_path': '/r9oTasGQofvkQY5vlUXglneF64Z.jpg', 'genre_ids': [28, 35], 'id': 1029575, 'original_language': 'en', 'original_title': 'The Family Plan', 'overview': "Dan Morgan is many things: a devoted husband, a loving father, a celebrated car salesman. He's also a former assassin. And when his past catches up to his present, he's forced to take his unsuspecting family on a road trip unlike any other.", 'popularity': 1853.509, 'poster_path': '/a6syn9qcU4a54Lmi3JoIr1XvhFU.jpg', 'release_date': '2023-12-14', 'title': 'The Family Plan', 'video': False, 'vote_average': 7.377, 'vote_count': 664}
    
    movie object look like this 
    grab title , gener ,poster , release_date , rating , overview
    Note: Dont save the movie in my Db 
    '''
    movies_list = []
    for movie in movies:
        title = movie.get('title', None)
        poster_path = movie.get('poster_path', None)
        overview = movie.get('overview', None)
        release_date = movie.get('release_date', None)
        vote_average = movie.get('vote_average', None)
        genre_ids = movie.get('genre_ids', None)
        genre = []
        for genre_id in genre_ids:
            genre.append(genre_id)
        movie_dict = {
            'title': title,
            'poster': f'https://image.tmdb.org/t/p/w500{poster_path}',
            'overview': overview,
            'release_date': release_date,
            'rating': vote_average,
            'genre': genre
        }
        movies_list.append(movie_dict)
    print(movies_list[0]['title'])
    context = {
        'movies': movies_list,
        'page': pages,
    } 
    return render(request, 'watchlist/movie_list.html', context)



def search_movie(request):
    query = request.GET.get('query')

    api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={query}'
    r = requests.get(api_url)
    data = r.json()
    movies = data['results']

    movies_list = []

    filtered_movies = [movie for movie in movies if query.lower() in movie['title'].lower()]

    for movie in filtered_movies:
        title = movie['title']
        poster_path = movie['poster_path']
        overview = movie['overview']
        release_date = movie['release_date']
        vote_average = movie['vote_average']
        genre_ids = movie['genre_ids']
        genre = [genre_id for genre_id in genre_ids]

        movie_dict = {
            'title': title,
            'poster': f'https://image.tmdb.org/t/p/w500{poster_path}',
            'overview': overview,
            'release_date': release_date,
            'rating': vote_average,
            'genre': genre
        }
        movies_list.append(movie_dict)

    context = {
        'movies': movies_list,
    } 
    return render(request, 'watchlist/search_movie.html', context)

