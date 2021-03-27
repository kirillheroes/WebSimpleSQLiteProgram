$(document).ready(function() {
	let updateForm = $('#update-task-form');
	// Обновление по нажатию
	updateForm.submit(function(event){
		// Отменяем событие, чтобы не было перехода на другую страницу
		event.preventDefault();
		let id = $(this).children("input[name='id']").val();
		// Считываем массив данных с формы
		let data = $(this).serializeArray().reduce(function(obj, item) {
    		obj[item.name] = item.value;
    		return obj;
		}, {});
		// Проверка на статус задания (чекбокс)
        data['status-input'] = (data['status-input']=='on') ? "true" : "false";

		$.ajax({
			url: '/task/'+id,
			type: 'PATCH',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify(data),
			success: function(result) {
                alert('Данные успешно обновлены!');
			}
		});
	});

	// Удаление задачи по нажатию на кнопку
	$('.delete-button').click(function() {
		// Получаем id задачи
        let id = $(this).parent().parent().parent().attr("data-id");

        $.ajax({
            url: '/task/'+id,
            type: 'DELETE',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'id':id}),
            success: function(result) {
                console.log(result);
            }
        });

        $(this).parent().parent().parent().remove();
    });

	// Комментарии
    let comments = $('#comments');
	if (comments) {
		let id = $('form').children("input[name='id']").val();
		$.ajax({
			type: 'get',
			url: 'https://jsonplaceholder.typicode.com/comments?postId='+id, 
			success: function(res) {
                res.forEach(function(elem){
             		// <div class="comment card-body bg-light mt-1">
					var comm_card = document.createElement('div');
					comm_card.className = 'comment card-body bg-light mt-1';
					
					// <h5 class="comment-name card-title text-info mb-0">${elem.name}</h5>
					var comm_auth = document.createElement('h5');
					comm_auth.className = 'comment-name card-title text-info mb-0';
					comm_auth.innerHTML = elem.name;

					// <h7 class="comment-email card-subtitle mb-2 text-muted">${elem.email}</h7>
					var comm_email = document.createElement('h7');
					comm_email.className = 'comment-email card-subtitle mb-2 text-muted';
					comm_email.innerHTML = elem.email;
					
					// <p class="comment-text card-text">${elem.body}</p>
					var comm_text = document.createElement('p');
					comm_text.className = 'comment-text card-text';
					comm_text.innerHTML = elem.body;
					
					comments.after(comm_card);
					comm_card.append(comm_auth);
					comm_card.append(comm_email);
					comm_card.append(comm_text);
				});
			}
		});
	}
});