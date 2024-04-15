import requests


class HeadHunterAPI:
    """ Класс для работы с API """
    def __init__(self, employers_ids: list):
        self.employers_ids = employers_ids
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "per_page": "100",
            "only_with_salary": "true"
        }

    def get_data(self) -> list[dict]:
        """
        Получение данных о вакансиях с hh.ru в формате JSON
        :return: Список с информацией о вакансиях
        """
        data = []

        for employer_id in self.employers_ids:
            self.params["employer_id"] = employer_id

            vacancies_data = self.__make_a_requests()
            data.append(vacancies_data)

            pages = vacancies_data.get("pages")
            if pages is not None:
                for num in range(1, pages):
                    self.params["page"] = num

                    vacancies_data = self.__make_a_requests()
                    data[-1]["items"].extend(vacancies_data.get("items"))

        return data

    def __make_a_requests(self) -> dict:
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
