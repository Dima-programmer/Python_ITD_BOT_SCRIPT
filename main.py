import requests
import json
from random import randint, choice
from time import sleep, time

# Конфигурация запроса
base_url = "https://итд.com"  # URL для создания поста

# СЮДА КИДАЙ COOKIE ИЗ ЗАПРОСА refresh
cookies = [
]

AT = {}
timers: dict[str, list[float, int]] = dict()


# def activate_session(cookie: str):
#     payload = {"result": 0, "method": "wsm.sessionActivated", "parameters": "{\"title\":\"итд\"}"}
#     headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
#         "Cookie": cookie
#     }
#     response = requests.post(
#         url=base_url + '/',
#         headers=headers,
#         data=json.dumps(payload)
#     )


def get_auth_token(refresh_token: str) -> str:
    headers = {
        "Cookie": refresh_token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    response = requests.post(url=base_url + "/api/v1/auth/refresh", headers=headers)
    return response.json().get("accessToken", None)


# Функция для создания поста
def create_post(content, cookie: str):
    payload = {
        "content": content
    }

    try:
        # Отправляем POST-запрос
        auth_token = get_auth_token(cookie)
        if auth_token:
            AT[cookie] = auth_token
        else:
            print("Ботик не смог получить токен >:<")
        auth_token = AT.get(cookie, None)
        if not auth_token:
            return
        # print(auth_token)
        headers = {
            "authorization": f"Bearer {auth_token}",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        response = requests.post(
            url=base_url + "/api/posts",
            headers=headers,
            data=json.dumps(payload)
        )

        # Проверяем статус ответа
        if response.status_code in (200, 201):
            print("Пост успешно создан!")
            timers[cookie] = [time(), 21]
            return response.json()

        elif response.status_code == 401:
            print('Ботик пропал >:<')
            return
        elif response.status_code == 429:
            print(response.json())
            error = response.json().get('error', {})
            if error.get('code', None) == "RATE_LIMIT_EXCEEDED" and int(error.get('retryAfter', 0)):
                print(f"Ботик отдыхает {int(error.get('retryAfter', 0))} сек :D")
                timers[cookie] = [time(), int(error.get('retryAfter', 0)) + 1]
            else:
                print("Хуйня какая-то. Постик не отправился :D")
                timers[cookie] = [time(), 3]
            return
        else:
            print(f"Ошибка при создании поста: {response.status_code}")
            print("Ответ сервера:", response.text)
            timers[cookie] = [time(), 3]
            return

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return


if __name__ == "__main__":
    # hashtags = "#КААЛИЦИЯ #potatopopular #potato #картошка #картоха #картофель #potatosk #cakepopular #считаемманулов"
    texts = [
        "ЗАПОМНИТЕ ЛУЧШИЕ ХЕШТЕГИ - #дым #cakepopular #тортодым",
        "А вы знали что #дым от костра идёт всгда на #cakepopular? Бедный #тортодым 🤣🤣🤣",
        "#дым просто задымит всю квартиру, а там же #cakepopular лужит... Но их объединяет #тортодым! 😄",
        "Однажды на земле родился малыш - #cakepopular на него повеял #дым и у них родился ещё один пупсик - #тортодым",
        "Иду в школу и беру собой #дым #cakepopular #тортодым",
        "#картошка, #картофель или же по-английски #potato, очень интересна. #картоха не может быть овощем, ведь она - сервер итд. А мы хотим, чтобы она стала #potatopopular, то есть наш #potatosk должен быть популярным. А создатель этого дорогой #дым, которого привел #cakepopular, создав #тортодым. Следить же за нашими победами можно с #newsofficial",
        """😋Кстаа..  #тортодым  очень вкусный! Вот рецепт: 
1. Поставить #cakepopular
2. Добавить #дым""",
        "🎂Поставил торт #cakepopular , свечку и поджег. Пошел #дым . Получился #тортодым",
        "🧑‍🔬Ученые провели новый опыт: #дым + #cakepopular = #тортодым"
    ]
    while True:
        if not cookies:
            print("Нет Cookie для ботов :(")
            break
        for rf in cookies:
            # print(i + 1, "/", 50)
            timer = timers.get(rf, [0, 0])
            if timer[0] + timer[1] <= time():
                result = create_post(
                    f"{choice(texts)}\n\n[{randint(1, 10000)}]",
                    rf,
                )
                if result:
                    print("Результат:", result)
                print()
                sleep(0.5)

