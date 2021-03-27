from flask import Flask, session, render_template, redirect, request, url_for
from entities import User
from entities import Task
from storage import Storage

# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'web34secretkeybrbrbrbr/'


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
    if not request.form['email']:
        error = 'Требуется ввести электронную почту!'
    elif not request.form['password']:
        error = 'Требуется ввести пароль!'
    elif not request.form['password2']:
        error = 'Требуется ввести повтор пароля!'
    elif request.form['password'] != request.form['password2']:
        error = 'Пароли не совпадают!'
    elif Storage.get_user_by_email(request.form['email']):
        error = 'Пользователь с таким email уже зарегистрирован!'

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
    # Удаляем пользователя из сессии
    session.pop('user_id')
    return redirect(url_for('home'))


# Вывод списка задач этого пользователя
@app.route('/tasks', methods=['GET'])
def show_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        tasks = Storage.get_task_by_user(user_id)
        return render_template('pages/task_list.html', page_title='Список задач', tasks=tasks, user=user)
    else:
        return redirect('/login')


# Добавление задачи       
@app.route('/task', methods=['GET'])
def new_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/new_task.html', page_title='Добавить задачу', user=user)
    else:
        return redirect('/login')


# Создание новой задачи
@app.route('/task', methods=['POST'])
def create_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)

        status = "false"
        if 'status-input' in request.form:
            status = "true"

        error = None
        if not request.form['title-input']:
            error = 'Необходимо ввести заголовок!'
        if error:
            return render_template('pages/new_task.html', page_title='Добавить задачу', error=error, user=user)
        Storage.add_task(Task(None, request.form['title-input'], request.form['description-input'], status, user))
        return redirect(url_for('show_tasks'))
    else:
        redirect(url_for('home'))


# Получение конкретной задачи
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        cur_task = Storage.get_task_by_id(task_id)
        return render_template('pages/task.html', page_title="Отредактировать задачу", task=cur_task, user=user)
    else:
        return redirect('/login')


# Обновление или удаление задачи
@app.route('/task/<int:task_id>', methods=['PATCH', 'DELETE'])
def task(task_id: int):
    # Обновление задачи
    if request.method == 'PATCH':
        if 'user_id' in session:
            user_id = session['user_id']
            user = Storage.get_user_by_id(user_id)
            dataObj = request.json

            status = "false"
            if dataObj['status-input'] == 1:
                status = "true"

            error = None
            if not dataObj['title-input']:
                error = 'Необходимо ввести заголовок!'
            if error:
                return render_template('pages/new_task.html', page_title='Обновить задачу', error=error, user=user)
            Storage.update_task(Task(dataObj['id'], dataObj['title-input'], dataObj['description-input'], status, None))
            return 'ok'
        else:
            redirect(url_for('home'))
    # Удаление задачи
    elif request.method == 'DELETE':
        if 'user_id' in session:
            user_id = session['user_id']
            Storage.delete_task(Task(int(request.json['id']), None, None, None, None))
            return 'ok'
        else:
            return redirect('/login')


if __name__ == '__main__':
    app.env = 'development'
    app.run(port=8080, host='127.0.0.1', debug=True)
