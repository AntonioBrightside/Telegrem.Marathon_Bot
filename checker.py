def answers_checker(answers: list) -> list:
    """
    Функция для обновления / добавления ответов пользователя в список для дальнейшей передачи этих данных в class Waiter.
    Проверяет на уровне выбора 'Завтрак' / 'Ужин', т.к. в дальнейшем у пользователя нет взможности (если не писать
    руками ингридиент) повлиять на список, передаваемый в Waiter.
    :param answers: список, составленный на основании ответов пользователя
    :return:
    """
    answers = [answer.replace('/breakfast', 'Завтрак') for answer in answers]
    answers = [answer.replace('/supper', 'Ужин') for answer in answers]
    if len(answers) == 1:
        return answers
    elif len(answers) == 3:
        return [answers[2]]
    elif 'Завтрак' and 'Ужин' in answers:
        return answers[1:]
