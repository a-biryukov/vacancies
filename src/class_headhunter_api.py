import requests


class HeadHunterAPI:
    """ Класс для работы с API """

    def get_data(self):
        """
        Получение данных о вакансиях с hh.ru в формате JSON
        :return: Список с информацией о работодателях и вакансиях
        """

        url = "https://api.hh.ru/vacancies"

        employers_ids = ["1740", "64174", "3529", "2748", "2180", "78638", "84585", "87021", "3127", "780654"]

        params = {
            "per_page": "100",
            "only_with_salary": "true"
        }

        data = []

        for employer_id in employers_ids:
            params["employer_id"] = employer_id

            vacancies_data = self.__make_a_requests(url, params)
            data.append(vacancies_data)

            pages = vacancies_data.get("pages")
            if pages is not None:
                for num in range(1, pages):
                    params["page"] = num

                    vacancies_data = self.__make_a_requests(url, params)
                    data[employers_ids.index(employer_id)]["items"].extend(vacancies_data.get("items"))

        return data

    @staticmethod
    def __make_a_requests(url: str, params: dict) -> dict:
        try:
            response = requests.get(url, params)
        except requests.ConnectionError as e:
            print("Ошибка подключения:", e)
        except requests.Timeout as e:
            print("Ошибка тайм-аута:", e)
        except requests.RequestException as e:
            print("Ошибка запроса:", e)
        else:
            data = response.json()

            return data


hh = HeadHunterAPI()

data_ = hh.get_data()

for employer in data_:
    if employer.get("items"):
        print(employer.get("items")[0].get("employer").get("name"))
        print(f"Количество вакансий: {employer.get("found")}")
        print()
    else:
        print("Ничего не найдено")
        print()
