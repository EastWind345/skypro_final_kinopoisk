import requests
from config import API_URL, API_TOKEN, BASE_URL


class ApiHelper:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            try:
                return response.json(), response.status_code
            except ValueError:
                return {"error": "Invalid JSON", "raw_response": response.text}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}, 0

    def search_movie(self, title):
        endpoint = "/api/v2.1/films/search-by-keyword"
        params = {"keyword": title}
        return self._make_request("GET", endpoint, params=params)

    def get_movie_reviews(self, movie_id):
        endpoint = f"/api/v2.1/films/{movie_id}/reviews"
        return self._make_request("GET", endpoint)

    def add_to_watchlist(self, movie_id):
        endpoint = "/api/v2.1/users/watchlist"
        data = {"filmId": movie_id}
        return self._make_request("POST", endpoint, json=data)

