from http import HTTPStatus

import requests


def handle_wrong_status(status_code: int) -> None:
    match status_code:
        case HTTPStatus.NOT_FOUND:
            print("Not found!")
        case HTTPStatus.BAD_REQUEST:
            print("Bad request!")
        case _:
            print(f"{status_code=}")


def task1() -> None:
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        print("Network error:", e)
        return

    if resp.status_code != HTTPStatus.OK:
        handle_wrong_status(resp.status_code)
        return

    try:
        data = resp.json()
    except ValueError:
        print("Invalid JSON in response")
        return

    first_five_titles = [post.get("title") for post in data[:5]]
    print(first_five_titles)


def task2() -> None:
    API_KEY = input("Введите API KEY: ")
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    city = input("Введите свой город: ")
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=7)
    except requests.RequestException as e:
        print("Network error:", e)
        return

    if resp.status_code != HTTPStatus.OK:
        handle_wrong_status(resp.status_code)

    try:
        data = resp.json()
    except ValueError:
        print("Invalid JSON")
        return

    temp = data.get("main", {}).get("temp")
    weather_desc = None
    weather_list = data.get("weather")
    if isinstance(weather_list, list) and weather_list:
        weather_desc = weather_list[0].get("description")

    print(f"Погода в {city}: {temp} °C, {weather_desc}")


def task3() -> None:
    payload = {"title": "My title", "body": "My body", "userId": 228}

    try:
        resp = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload, timeout=7)
    except requests.RequestException as e:
        print("Network error:", e)
        return

    if resp.status_code != HTTPStatus.CREATED:
        handle_wrong_status(resp.status_code)

    try:
        data = resp.json()
    except ValueError:
        print("Invalid JSON in response")
        return
    created_id = data.get("id")
    print("Создан пост:")
    print("ID:", created_id)
    print("Ответ сервера:", data)
