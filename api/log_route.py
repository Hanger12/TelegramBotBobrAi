import json
from datetime import datetime

from flask import Flask, jsonify, request
from db.repository import get_logs, get_logs_by_user
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/logs', methods=['GET'])
def logs():
    """
        Получить список всех запросов.
        ---
        responses:
          200:
            description: Список всех запросов.
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    description: ID пользователя.
                  command:
                    type: string
                    description: Команда, которую отправил пользователь.
                  timestamp:
                    type: string
                    description: Дата и время запроса.
                  response:
                    type: string
                    description: Ответ бота.
          500:
            description: Ошибка сервера.
        """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Получаем параметры для фильтрации по времени
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Преобразуем строки в объекты datetime, если они указаны
    if start_time:
        start_time = datetime.fromisoformat(start_time)
    if end_time:
        end_time = datetime.fromisoformat(end_time)

    logs = get_logs(page, per_page, start_time, end_time)
    if not logs:
        response = app.response_class(
            response=json.dumps({"error": "Логи не найдены"}, ensure_ascii=False),
            status=200,
            mimetype='application/json; charset=utf-8'
        )
        return response, 404

    response_data = [{
        "user_id": log.user_id,
        "command": log.command,
        "response": log.response,
        "timestamp": log.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    } for log in logs]
    response = app.response_class(
        response=json.dumps(response_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )

    return response


@app.route('/logs/<int:user_id>', methods=['GET'])
def logs_by_user(user_id):
    """
        Получить запросы конкретного пользователя.
        ---
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            description: ID пользователя для получения его запросов.
        responses:
          200:
            description: Список запросов конкретного пользователя.
            schema:
              type: array
              items:
                type: object
                properties:
                  command:
                    type: string
                    description: Команда, которую отправил пользователь.
                  timestamp:
                    type: string
                    description: Дата и время запроса.
                  response:
                    type: string
                    description: Ответ бота.
          404:
            description: Логи не найдены для данного пользователя.
          500:
            description: Ошибка сервера.
    """
    page = request.args.get('page', 1, type=int)

    # Получаем параметры для фильтрации по времени
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Преобразуем строки в объекты datetime, если они указаны
    if start_time:
        start_time = datetime.fromisoformat(start_time)
    if end_time:
        end_time = datetime.fromisoformat(end_time)

    logs = get_logs_by_user(user_id, page, start_time, end_time)
    # Если логи не найдены, возвращаем 404
    if not logs:
        response = app.response_class(
            response=json.dumps({"error": "Логи не найдены для данного пользователя"}, ensure_ascii=False),
            status=200,
            mimetype='application/json; charset=utf-8'
        )
        return response, 404

    response_data = [{
        "user_id": log.user_id,
        "command": log.command,
        "response": log.response,
        "timestamp": log.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    } for log in logs]

    response = app.response_class(
        response=json.dumps(response_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )

    return response
