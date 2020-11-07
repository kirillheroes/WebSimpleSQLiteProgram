class User:
    """Класс пользователя
    :param id: идентификатор
    :type id: int
    :param email: эдектронная почта
    :type email: str
    :param password: пароль
    :type password: str"""
    def __init__(self, id: int, email: str, password: str):
        self.id = id
        self.email = email
        self.password = password


class Task:
    """Класс задания
    :param id: идентификатор
    :type id: int
    :param user_id: идентификатор пользователя
    :type user_id: int
    :param title: заголовок
    :param title: str
    :param completed: статус
    :param completed: bool
    :param description: описание
    :param description: str"""
    def __init__(self, id: int, user_id: int, title: str, description: str, completed: bool):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.completed = completed
