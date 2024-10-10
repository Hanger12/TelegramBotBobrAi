from sqlalchemy import and_

from db.models import Log, UserSettings, engine
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


def log_request(user_id, command, response):
    # Проверяем, существует ли пользователь с таким user_id в user_settings
    user_setting = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()

    if not user_setting:
        # Если нет настроек для этого пользователя, создаем их по умолчанию
        default_user_settings = UserSettings(user_id=user_id, default_city=None)
        session.add(default_user_settings)
        session.commit()

    # Логируем запрос
    log = Log(user_id=user_id, command=command, response=response)
    session.add(log)
    session.commit()


def save_user_settings(user_id: int, city: str):
    """Сохраняет выбранный город пользователя."""
    session = Session()
    user_setting = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if user_setting:
        user_setting.default_city = city
    else:
        user_setting = UserSettings(user_id=user_id, default_city=city)
        session.add(user_setting)
    session.commit()
    session.close()


def get_user_settings(user_id: int) -> str:
    """Получает настройки пользователя."""
    session = Session()
    user_setting = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    session.close()
    return user_setting.default_city if user_setting else None


def get_logs(page, per_page, start_time=None, end_time=None):
    """Возвращает список логов с пагинацией и фильтрацией по времени."""
    session = Session()
    query = session.query(Log)

    # Применяем фильтрацию по времени, если указаны даты
    if start_time and end_time:
        query = query.filter(and_(Log.timestamp >= start_time, Log.timestamp <= end_time))

    logs = query.order_by(Log.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()
    session.close()
    return logs


def get_logs_by_user(user_id, page, start_time=None, end_time=None):
    """Возвращает логи конкретного пользователя с пагинацией и фильтрацией по времени."""
    session = Session()
    query = session.query(Log).filter(Log.user_id == user_id)

    # Применяем фильтрацию по времени, если указаны даты
    if start_time and end_time:
        query = query.filter(and_(Log.timestamp >= start_time, Log.timestamp <= end_time))

    logs = query.order_by(Log.timestamp.desc()).offset((page - 1) * 10).limit(10).all()  # 10 логов на страницу
    session.close()
    return logs
