import requests
from typing import Any


class HeadHunterAPI:
    """ Класс для работы с API """

    employers_ids: list[str]

    def __init__(self, employers_ids: list[str]) -> None:
        """
        Конструктор класса. Задаем значения атрибутам экземпляра класса.
        :param employers_ids: Список с id компаний
        """
        self.employers_ids = employers_ids
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "per_page": "100",
            "only_with_salary": "true"
        }

    def get_data(self) -> list[dict[str: Any]]:
        """
        Получение данных о вакансиях с hh.ru в формате JSON
        :return: Список с информацией о вакансиях
        """
        data = []

        for employer_id in self.employers_ids:
            self.params["employer_id"] = employer_id

            vacancies_data = self.__make_a_request()
            data.append(vacancies_data)

            pages = vacancies_data.get("pages")
            if pages is not None:
                for num in range(1, pages):
                    self.params["page"] = num

                    vacancies_data = self.__make_a_request()
                    data[-1]["items"].extend(vacancies_data.get("items"))

            del self.params["page"]

        return data

    def __make_a_request(self) -> dict[str: Any]:
        """ Делает запрос, отрабатывает ошибки и возвращает данные в формате JSON"""
        try:
            response = requests.get(self.url, self.params)
        except requests.ConnectionError as e:
            print("Ошибка подключения:", e)
        except requests.Timeout as e:
            print("Ошибка тайм-аута:", e)
        except requests.RequestException as e:
            print("Ошибка запроса:", e)
        else:
            data = response.json()

            return data
