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
    """Класс задачи
    :param id: идентификатор
    :type id: int
    :param title: заголовок задачи
    :type title: str
    :param description: описание задачи
    :type description: str
    :param status: статус задачи
    :type description: text
    :param user: пользователь
    :type user: User"""
    def __init__(self, id: int, title: str, description: str, status: str, user: User):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.user = user