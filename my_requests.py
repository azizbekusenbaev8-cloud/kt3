import requests
import pprint

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, json=None, expected_error=False):
        response = None
        for attempt in range(3):
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=json)
            elif request_type == 'PUT':
                response = requests.put(url, json=json)
            elif request_type == 'DELETE':
                response = requests.delete(url)

            if (not expected_error and response.status_code == 200) or expected_error:
                break

        pprint.pprint(f'--- {request_type} ---')
        pprint.pprint(response.url)
        pprint.pprint(f"Status: {response.status_code}")
        
        try:
            pprint.pprint(response.json())
        except Exception:
            pprint.pprint(response.text)
            
        pprint.pprint('**********')
        return response

    def get(self, endpoint, endpoint_id="", expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id:
            url += f'/{endpoint_id}'
        return self._request(url, 'GET', expected_error=expected_error)

    def post(self, endpoint, body, endpoint_id=""):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id:
            url += f'/{endpoint_id}'
        return self._request(url, 'POST', json=body)

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        return self._request(url, 'PUT', json=body)

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        return self._request(url, 'DELETE')


if __name__ == "__main__":
    print("=== СТАРТ ТЕСТИРОВАНИЯ ===")
    api = BaseRequest("https://petstore.swagger.io/v2")

    print("\n>>> ТЕСТЫ ДЛЯ USER <<<")
    username = "student_test_2026_v2"
    
    user_data = {
        "id": 123,
        "username": username,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "email": "old_email@test.com",
        "password": "password123",
        "phone": "79990000000",
        "userStatus": 1
    }
    res = api.post("user", user_data)
    assert res.status_code == 200, "Ошибка при создании user"

    res = api.get("user", username)
    assert res.status_code == 200, "Не удалось получить user"
    assert res.json()["username"] == username, "Имя пользователя не совпадает!"
    
    user_data["email"] = "new_email@test.com"
    res = api.put("user", username, user_data)
    assert res.status_code == 200, "Ошибка при обновлении user (PUT)"
    
    res = api.get("user", username)
    assert res.json()["email"] == "new_email@test.com", "Email не обновился!"

    res = api.delete("user", username)
    assert res.status_code == 200, "Ошибка при удалении user"
    
    res = api.get("user", username, expected_error=True)
    assert res.status_code == 404, "Пользователь не удалился, сервер не вернул 404!"


    print("\n>>> ТЕСТЫ ДЛЯ STORE <<<")
    order_id = 5
    
    res = api.get("store/inventory")
    assert res.status_code == 200, "Не удалось получить инвентарь"

    order_data = {
        "id": order_id,
        "petId": 10,
        "quantity": 1,
        "shipDate": "2023-10-27T10:00:00.000Z",
        "status": "placed",
        "complete": True
    }
    res = api.post("store/order", order_data)
    assert res.status_code == 200, "Ошибка при создании заказа"

    res = api.get("store/order", order_id)
    assert res.status_code == 200, "Не удалось получить заказ"
    assert res.json()["id"] == order_id, "ID заказа не совпадает!"

    res = api.delete("store/order", order_id)
    assert res.status_code == 200, "Ошибка при удалении заказа"
    
    res = api.get("store/order", order_id, expected_error=True)
    assert res.status_code == 404, "Заказ не удалился, сервер не вернул 404!"

    print("\n=== ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ===")