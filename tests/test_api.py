import unittest
from flask import json
from api.log_route import app
from db.repository import log_request


class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Запускает один раз перед всеми тестами."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

    def test_get_all_logs(self):
        """Тест для получения всех логов."""
        response = self.client.get('/logs?page=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)  # Убедитесь, что возвращаемые данные - это список

    def test_get_logs_by_user(self):
        """Тест для получения логов конкретного пользователя."""
        user_id = 123
        command = "/weather Moscow"
        response = "Погода в Moscow: ..."
        log_request(user_id, command, response)  # Для начала добавим логи для пользователя
        response = self.client.get(f'/logs/{user_id}?page=1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_logs_by_nonexistent_user(self):
        """Тест для получения логов несуществующего пользователя."""
        user_id = 999999
        response = self.client.get(f'/logs/{user_id}?page=1')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == '__main__':
    unittest.main()
