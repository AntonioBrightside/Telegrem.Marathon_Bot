import json
from to_test.components_and_pairs import BREAKFAST_PAIRS, SUPPER_PAIRS


class Waiter:
    """
    Данный класс служит связующим между телеграм ботом и БД.
    По запросу бота (на основании выбранных пользователем ингридиентов) класс отдаёт боту меню
    """

    def __init__(self, user_id: int, answers: list):
        self.id = user_id
        self.answers = answers
        self.set_message()

    def __repr__(self):
        return self.message  # ','.join(map(str, self.__menu(self.answers)))

    def __len__(self):
        return len(self)

    def __iter__(self):
        return self  # iter(self.__menu(self.answers))  # TODO: Переписать, должно возвращать self

    def set_message(self) -> str:
        """
        Данны метод использует функцию menu(), тем самым принимает список блюд, компонентов и их описание.
        И отдает ТГ боту форматированную строку с меню
        :return: string
        """
        self.message = ''
        self.pair, self.description = self.__menu(self.answers)

        if self.meal == 'Завтрак':
            for dish in self.pair:
                if dish in self.description:
                    self.message = self.message + '\U0001F374' + dish + '\n'  # одинаковый блок кода_1
                    complst = self.description[self.description.index(dish) + 1]
                    if type(complst) == list:
                        for component in complst:
                            self.message = self.message + f' - {component}\n'
                    self.message = self.message + self.description[self.description.index(dish) + 2] + '\n'
                else:
                    self.message = self.message + '\U0001F374' + dish + '\n\n'

        elif self.meal == 'Ужин':
            for dish in self.pair:
                if len(self.pair) == 2 and dish in self.description:
                    self.message = self.message + '\U0001F374' + dish + '\n'  # одинаковый блок кода_1
                    complst = self.description[self.description.index(dish) + 1]
                    if type(complst) == list:
                        for component in complst:
                            self.message = self.message + f' - {component}\n'
                    self.message = self.message + self.description[self.description.index(dish) + 2] + '\n'

                elif dish in self.description[0]:
                    self.message = self.message + '\U0001F374' + dish + '\n'
                    dishindex = self.description[0].index(dish)
                    complist = self.description[1][dishindex]
                    if type(complist) == list:
                        for component in complist:
                            self.message = self.message + f' - {component}\n'
                    self.message = self.message + self.description[2][dishindex] + '\n\n'
                else:
                    self.message = self.message + '\U0001F374' + dish + '\n\n'

        return self.message

    def __menu(self, answers: list) -> tuple:
        """
        Метод, который принимает первоначальные данные от бота для дальнейшей обработки.
        :param answers: список ответов пользователя на вопросы бота. К примеру:['Завтрак', 'кабачки']
        :return:
        """
        self.meal, self.component = answers
        self.result = self.__for_menu(self.meal, self.component)
        self.pair = self.__pair(self.result[0])

        return self.pair, self.result

    @staticmethod
    def __load_breakfast() -> tuple[dict, dict]:
        """
        Загружаем тестовые данные для Завтрака для сопоставления ответов пользователя и ингридиентов / блюд меню.
        :return:
        """
        with open(r'to_test/breakfast_dishes_and_components.json', 'r', encoding='utf8') as f:
            dishes = json.load(f)

        with open('to_test/breakfast_description.json', 'r', encoding='utf8') as f:
            description = json.load(f)

        return dishes, description

    @staticmethod
    def __load_supper() -> tuple[dict, dict]:
        """
        Загружаем тестовые данные для Ужина для сопоставления ответов пользователя и ингридиентов / блюд меню.
        :return:
        """
        with open(r'to_test/supper_dishes_and_components.json', 'r', encoding='utf8') as f:
            dishes = json.load(f)

        with open(r'to_test/supper_description.json', 'r', encoding='utf8') as f:
            description = json.load(f)

        return dishes, description

    def __for_menu(self, meal: str, component: str) -> tuple:
        """
        Метод отдает кортеж / строки  с названием блюда, его компонентами, описанием приготовления.
        :param meal: период приема пищи ("Завтрак" или "Ужин")
        :param component:  выбранный пользователем компонент, на основе которого предлагается блюдо
        :return: tuple
        """
        self.bdishes, self.bdescription = self.__load_breakfast()
        self.sdishes, self.sdescription = self.__load_supper()

        if meal == 'Завтрак':
            for k, v in self.bdishes.items():
                if component in v:
                    self.dish = k
                    self.dish_components = v

            for k, v in self.bdescription.items():
                if self.dish == k:
                    self.description = v

        elif meal == 'Ужин':
            splcomp = component.split(' и ')
            self.dish = []
            self.dish_components = []
            self.description = []
            for k, v in self.sdishes.items():
                if len(splcomp) == 1 and component in v:
                    self.dish = k
                    self.dish_components = v
                else:
                    for comp in splcomp:
                        if comp in v:
                            self.dish.append(k)
                            self.dish_components.append(v)

            for k, v in self.sdescription.items():
                if len(splcomp) == 1 and self.dish == k:
                    self.description = v
                elif k in self.dish:
                    self.description.append(v)

        return self.dish, self.dish_components, self.description

    def __pair(self, dish: str | list) -> list:
        self.dish = dish
        if self.meal == 'Завтрак' and type(dish) == str:
            for pair in BREAKFAST_PAIRS:
                if self.dish in pair:
                    return pair
        elif type(dish) == str:
            for pair in SUPPER_PAIRS:
                if self.dish in pair:
                    return pair
        elif type(dish) == list:
            for pair in SUPPER_PAIRS:
                if self.dish[0] in pair:
                    return pair


# to_CHECK
if __name__ == '__main__':
    lst = ['Завтрак', 'кабачки']
    st_check = ['Ужин', 'свинина (вырезка) и  белокочанная капуста']

    print(Waiter(2, st_check))
