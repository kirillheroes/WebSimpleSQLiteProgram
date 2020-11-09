import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from entities import User, Task

# Подключаемся к БД
db_path = '/'.join([str(Path(__file__).parent), '..', 'db', 'database.sqlite'])
db = sqlite3.connect(db_path, check_same_thread=False)


class Storage:
    @staticmethod
    def add_user(user: User):
        """Добавление пользователя
        :param user:    новый пользователь
        :type user:     User"""
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email: str, passwordHash: str) -> User:
        """Найти пользователя по email и паролю
        :param email:       электронная почта
        :type email:        str
        :param passwordHash:    хэш пароля
        :type passwordHash:     str
        :return: пользователь
        :rtype: User
        """
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], passwordHash):
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_by_id(id: int) -> User:
        """Найти пользователя по id
        :param id:  идентификатор пользователя
        :type id:   int
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_tasks_by_id(id: int) -> list:
        """Получение списка всех заданий у определённого пользователя по его id
        :param id: идентификатор пользователя
        :type id: int
        :return: список заданий
        :rtype: list"""
        user_tasks = db.execute('SELECT * FROM tasks WHERE user_id=?', (id,)).fetchall()
        if user_tasks:
            tasks_list = []
            for task in user_tasks:
                tasks_list.append(Task(id=task[4], user_id=task[0],
                                       title=task[1], description=task[2], completed=task[3]))
            return tasks_list
        else:
            return None

    @staticmethod
    def add_task(task: Task):
        """Добавление пользователя
        :param task:    новое задание
        :type task:     Task"""
        db.execute('INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)',
                   (task.user_id, task.title, task.description))
        db.commit()

    @staticmethod
    def get_task_by_id(id: int) -> Task:
        """Получение конретного задания по его id
        :param id: идентификатор задания
        :type id: int
        :return: задание
        :rtype: Task"""
        task = db.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchall()[0]
        return Task(id=task[4], user_id=task[0], title=task[1], description=task[2], completed=task[3])

    @staticmethod
    def update_task_by_id(id: int, title: str, desc: str, done: bool):
        """Обновление задания
        :param id: идентификатор задания
        :type id: int
        :param title: новый заголовок задания
        :type title: str
        :param desc: новое описание задания
        :type desc: str
        :param done: статус задания
        :type done: bool"""
        db.execute("UPDATE tasks SET title=?, description=?, completed=? WHERE id=?", (title, desc, done, id,))
        db.commit()

