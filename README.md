# AgentKM
Автоматизация работы агентов

-------------------------------------
## Подготовка проекта к запуску:
### Redis
1. Установить Redis: 
	sudo apt install redis-server
2. В настройках указать прослушивание всех ip:
	sudo nano /etc/redis/redis.conf
	Закомментировать bind 127.0.0.1 ::1
3. В настройках отключить защищенный режим:
	protected-mode no
4. Включить автозапуск:
	sudo systemctl enable redis-server
5. Включить Redis:
	sudo systemctl start redis-server
-------------------------------------
### Celery:
1. Запуск celery:
	celery -A Agent_mobile worker -l INFO --pool=solo
2. Запуск рассписания: 
	celery -A Agent_mobile beat
