from flask import Flask, session, render_template, redirect, request, url_for
from entities import User, Task
from storage import Storage

# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'_5#y2L"F4Q8ziDec]/'


# Описываем основные маршруты и их обработчики

# Главная страница
@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/index.html', user=user)
    else:
        return redirect('/login')


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='Auth Example')


# Обработка формы входа
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход / Auth Example'

    # Введённые данные получаем из тела запроса
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести email')
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести пароль')

    # Ищем пользователя в БД с таким email паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверный пароль
    if not user:
        return render_template('pages/login.html', page_title=page_title, error='Неверный пароль')

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация / Auth Example')


# Обработка формы регистрации
@app.route('/registration', methods=['POST'])
def registration_action():
    page_title = 'Регистрация | Auth Example'
    error = None
    # Проверяем данные
    if request.form['password'] != request.form['password2']:
        error = 'Пароли не совпадают'
    if not request.form['password2']:
        error = 'Требуется ввести повтор пароля'
    if not request.form['password']:
        error = 'Требуется ввести пароль'
    if not request.form['email']:
        error = 'Требуется ввести Email'

    # В случае ошибки рендерим тот же шаблон, но с текстом ошибки
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)

    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))

    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))


# Страница с заданиями
@app.route('/tasks', methods=['GET'])
def tasks():
    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)
    tasks_list = Storage.get_user_tasks_by_id(user_id)
    if tasks_list is None:
        tasks_list = []
    return render_template('pages/tasks.html', user=user, tasks=tasks_list, page_title='Задачи / Auth Example')


@app.route('/task', methods=['GET'])
def new_task_info():
    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)
    return render_template('pages/add_task.html', user=user, page_title='Добавление задания / Auth Example')


@app.route('/task', methods=['POST'])
def add_task():
    page_title = 'Добавление задания | Auth Example'

    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)

    # Проверяем данные
    if not request.form['title']:
        return render_template('pages/add_task.html',
                               page_title=page_title, user=user, error='Требуется ввести заголовок')
    if not request.form['description']:
        return render_template('pages/add_task.html',
                               page_title=page_title, user=user, error='Требуется ввести описание')

    user_id = session['user_id']
    new_task = Task(None, user_id, request.form['title'], request.form['description'], 0)

    Storage.add_task(new_task)

    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на задания
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)
    task = Storage.get_task_by_id(task_id)
    return render_template('pages/edit_task.html',
                           user=user, task=task, page_title='Редактирование задания / Auth Example')


@app.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    page_title = 'Редактирование задания | Auth Example'

    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)
    task = Storage.get_task_by_id(task_id)

    # Проверяем данные
    if not request.form['title']:
        return render_template('pages/edit_task.html',
                               page_title=page_title, task=task, user=user, error='Требуется ввести заголовок')
    if not request.form['description']:
        return render_template('pages/edit_task.html',
                               page_title=page_title, task=task, user=user, error='Требуется ввести описание')

    Storage.update_task_by_id(task_id, request.form['title'], request.form['description'])

    # Делаем вид, что обновление всегда без ошибки
    # Перенаправляем на задания
    return redirect(url_for('tasks'))


if __name__ == '__main__':
    app.env = 'development'
    app.run(port=8080, host='127.0.0.1', debug=True)

