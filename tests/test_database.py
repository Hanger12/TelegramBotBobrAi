import unittest
from db.repository import log_request, save_user_settings, get_user_settings, Session
from db.models import Log, UserSettings


class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Фикстура для настройки базы данных перед тестами."""
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        """Фикстура для очистки базы данных после тестов."""
        cls.session.query(Log).delete()
        cls.session.query(UserSettings).delete()
        cls.session.commit()
        cls.session.close()

    def test_log_request(self):
        """Тест для функции логирования запросов."""
        user_id = 123
        command = "/weather Moscow"
        response = "Погода в Moscow: ..."

        log_request(user_id, command, response)

        log = self.session.query(Log).filter_by(user_id=user_id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.command, command)
        self.assertEqual(log.response, response)

    def test_save_user_settings(self):
        """Тест для функции сохранения настроек пользователя."""
        user_id = 124
        city = "Moscow"

        save_user_settings(user_id, city)

        user_setting = self.session.query(UserSettings).filter_by(user_id=user_id).first()
        self.assertIsNotNone(user_setting)
        self.assertEqual(user_setting.default_city, city)

    def test_get_user_settings_existing(self):
        """Тест для получения настроек существующего пользователя."""
        user_id = 125
        city = "Moscow"

        save_user_settings(user_id, city)
        retrieved_city = get_user_settings(user_id)
        self.assertEqual(retrieved_city, city)

    def test_get_user_settings_non_existent(self):
        """Тест для получения настроек несуществующего пользователя."""
        user_id = 999
        retrieved_city = get_user_settings(user_id)
        self.assertIsNone(retrieved_city)


if __name__ == "__main__":
    unittest.main()
