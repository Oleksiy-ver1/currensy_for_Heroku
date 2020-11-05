import requests
from bs4 import BeautifulSoup  # из bs4 вытаскиваем BeautifulSoup


class Parser:
    def __init__(self, url):  # Инициализация экземпляра класса
        # headers убрал из конфига, так как он не будет меняться и нужен только здесь
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.132 "
                          "Safari/537.36",
            "accept": "*/*"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            bs_text = response.text
        else:
            bs_text = ''
        # Если ответ не 200, то передаем в bs пустую строку. И наши ответы будут пустые строки.
        self.soup = BeautifulSoup(bs_text, 'html.parser')  # создаем экземпляр BeautifulSoup с обработкой ответа
        self._get_addres()
        self._get_course()
        self._get_phone()

    def _get_phone(self):
        self.phones = []
        items_phone = self.soup.findAll("div", {"class": "headerdivphone"})  # добываем номера телефонов
        for item in items_phone:
            self.phones.append(item.find('a').get('href'))

    def _get_addres(self):
        address = self.soup.find("a", {"href": "#address"})
        self.address = address.getText('span').replace('span', '').replace('\n', '').strip()

    def _get_course(self):
        items_currency = self.soup.findAll("span", {"class": "indexspancurrency"})
        items = self.soup.findAll("span", {"class": "indexspanbuy"})
        self.course = self._combine_dic(items, items_currency)

    def _combine_dic(self, items, items_currency):
        half_dic1 = self._creating_dictionary1(items)
        half_dic2 = self._creating_dictionary2(items_currency)
        return dict(zip(half_dic2, half_dic1))

    @staticmethod
    def _creating_dictionary1(items):
        k = []
        half_dic = []
        for item in items:
            k.append(item.text.strip())
        for elem in range(2, len(k), 2):
            half_dic.append(str(k[elem]) + '/' + str(k[elem + 1]))
        return half_dic

    @staticmethod
    def _creating_dictionary2(items_currency):
        half_dic = []
        for item in items_currency:
            half_dic.append(item.text.strip().replace(' ', '').replace('\n', '/'))
        half_dic = half_dic[1:]
        return half_dic
