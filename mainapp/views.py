from django.shortcuts import render
from tmdbv3api import TMDb, Movie, Discover
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

tmdb = TMDb()
tmdb.api_key = 'db5fb45ba4e01969dd293a217985b358'

genres = {'28': 'Action', '12': 'Adventure', '16': 'Animation', '35': 'Comedy', 
		  '80': 'Crime', '99': 'Documentary', '18': 'Drama', '10751': 'Family', 
		  '14': 'Fantasy', '36': 'History', '27': 'Horror', '10402': 'Music',
		  '9648': 'Mystery', '10749': 'Romance', '878': 'ScienceFiction',
		  '10770': 'TVMovie', '53': 'Thriller', '10752': 'War', '37': 'Western'}

def serialize_movie_array(m, limit):
	k = []
	for i in m:
		if i['original_language'] == "en" or i ['original_language'] == "hi":
			i = dict(i)
			if len(i['title'])>30:
				i['title'] = i['title'][:30] + "..."
			genres_str = ""
			if len(i["genre_ids"])>3:
				i["genre_ids"] = i["genre_ids"][:3]
			for j in i["genre_ids"]:
				genres_str += genres[str(j)] + ", "
			genres_str = genres_str[:-2]
			mdict =  {'title':i['title'], 'image': 'https://image.tmdb.org/t/p/w500'+str(i['poster_path']),
					'genre':genres_str,"id": i["id"], 'rating':i['vote_average'], 'overview': i['overview']}
			k.append(mdict)
		if len(k) == limit:
			break
	return k

def serialize_hindi_movie(m):
	k = []
	for i in m:
		mdict = {}
		i = dict(i)
		if len(i['title'])>30:
			i['title'] = i['title'][:30] + "..."
		genres_str = ""
		if len(i["genre_ids"])>3:
			i["genre_ids"] = i["genre_ids"][:3]
		for j in i["genre_ids"]:
			genres_str += genres[str(j)] + ", "
		genres_str = genres_str[:-2]
		if "/" not in i["original_title"]:
			title = i["original_title"]
		else:
			title = i["title"]
		mdict = {'title': title, 'image': 'https://image.tmdb.org/t/p/w500'+str(i['poster_path']),
				'genre':genres_str,'id':i['id'], 'rating':i['vote_average'], 'overview': i['overview']}
		k.append(mdict)
	return k


def serialize_movie_details(id):
	m = Movie()
	k = m.details(int(id))
	casts = []
	if len(k.casts["cast"])>20:
		k.casts["cast"] = k.casts["cast"][:20]
	for i in k.casts["cast"]:
		try:
			casts.append({'name':i['name'], 'character': i['character'], 'image': 'https://image.tmdb.org/t/p/w500' + i['profile_path']})
		except:
			casts.append({'name':i['name'], 'character': i['character']})
	director = ""
	for i in k.casts["crew"]:
		if i["job"] == "Director":
			director += i['name']
	genres_str = ""
	for j in k.genres:
		genres_str += j['name'] + ", "
	genres_str = genres_str[:-2]
	response = {'title':k.original_title, 'director': director, 'year': str(k.release_date)[:4], 'runtime': k.runtime,
				'genres': genres_str, 'rating' : k.vote_average, 'backdrop' : 'https://image.tmdb.org/t/p/w500' + k.backdrop_path,
				'poster':'https://image.tmdb.org/t/p/w500'+k.poster_path,'summary':k.overview, 'casts':casts}
	similar = m.similar(int(id))
	if len(similar)>10:
		similar = similar[:10]
	similar_movies = []
	for i in similar:
		if len(i['title'])>30:
			i['title'] = i['title'][:30] + "..."
		genres_str = ""
		if len(i["genre_ids"])>3:
			i["genre_ids"] = i["genre_ids"][:3]
		for j in i["genre_ids"]:
			genres_str += genres[str(j)] + ", "
		genres_str = genres_str[:-2]
		similar_movies.append({'title':i['title'], 'poster':'https://image.tmdb.org/t/p/w500'+i['poster_path'],
							   'genres':genres_str, 'id':i["id"], 'year': str(k.release_date)[:4]})
	return [response,similar_movies]

@csrf_exempt
def search(request):
	if request.method == "POST":
		movie = Movie()
		results = serialize_movie_array(movie.search(request.POST["search"]),5)
		if len(results)>5:
			return JsonResponse({"results":results[:5]})
		else:
			return JsonResponse({"results":results})

def main(request):
	movie = Movie()
	d = Discover()
	popular_movies = serialize_movie_array(movie.popular(),10)
	playing_now = serialize_movie_array(movie.now_playing(),10)
	hindi_movies = serialize_hindi_movie(d.discover_movies({"with_original_language":"hi",'vote_count.gte': 100, 'sort_by': 'vote_average.desc'})[:10])
	return render(request, 'index.html', {'popular_movies':popular_movies, 'playing_now':playing_now, 'hindi_movies':hindi_movies})


def movie_details(request, id):
	response = serialize_movie_details(id)
	return render(request, 'movie.html', {'response':response[0], 'similar_movies':response[1]})