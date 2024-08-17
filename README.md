# Проектная работа 10 спринта: ONLINE CINEMA SERVICE (Notifications)

## [Ссылка на репозиторий](https://github.com/SmirnovaT/notifications_sprint_1)

## Структура проекта

- [Airflow](airflow) для отправки регуляных уведомлений
- [API](notification_service/src) для принятия данных для уведолений от других сервисов. (Принимает и кладет в очередь.)
- [Event Worker](notification_service/src/event_worker) основной обработчик нотификационных событий. (Слушает
  сообщения из очереди, определяет тип, обогащает данными, рендерит шаблон, cоздает нотификации в mongodb, мгновенные
  отправляет сразу в очередь)
- [Scheduler Worker](scheduler_worker) проверяет в mongodb готовность сообщений к отправке и кладет их в очередь
- [Sender Worker](sender_worker) слушает сообщения из очереди и отправляет пользователям

## Запуск проекта

### Запуск приложения в контейнере из корня проекта

```
docker compose up --build -d
```

### Запуск приложения для локальной разработки
```
1. cp .env.prod.example .env
2. python3.11 -m venv venv
3. source venv/bin/activate
4. pip3 install poetry
5. python -m poetry install
6. cd notification_service
7. uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Работа с RabbitMQ

Запустить контейнер локально

```
docker run --rm -p 15672:15672 rabbitmq:3.10.7-management
```

Открыть веб-интерфейс RabbitMQ в браузере
(login - guest, password - guest)
```
http://127.0.0.1:15672/
```

### Запуск тестов

Необходимо поменять в .env значение переменной RABBITMQ_HOST=test-rabbitmq
```
1. cd notification_service/src/tests
2. docker-compose up --build
3. poetry run pytest
 ```
### Настройка регулярных оповещений в Airflow

```
1. переименуйте .env.example в .env
2. Авторизуйтесь в интерфейсе airflow http://localhost:8080
	Логин: airflow
	пароль: airflow
3. В переменных задайте желаемое сообщение и дату доставки рассылки.
4. Запустите DAG "send news"
```