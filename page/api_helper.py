import requests
from config import API_URL, API_TOKEN, TIMEOUT


class ApiHelper:
    def __init__(self):
        if not API_TOKEN:
            raise ValueError("API_TOKEN не задан!")
        self.api_url = API_URL.rstrip('/')
        self.headers = {"X-API-KEY": API_TOKEN.strip()}

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(
                method=method, url=url, headers=self.headers, timeout=TIMEOUT,
                **kwargs
            )
            try:
                data = response.json()
            except ValueError:
                data = {"response_text": response.text[:500]}
            return data, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 0

    def search_movie(self, title):
        return self._request("GET", "api/v2.1/films/search-by-keyword",
                             params={"keyword": title})

    def get_movie_reviews(self, movie_id):
        return self._request("GET", f"api/v2.1/films/{movie_id}/reviews")

    def add_to_watchlist(self, movie_id):
        return self._request("POST", "api/v2.1/users/watchlist",
                             json={"filmId": movie_id})
