from datetime import datetime
import requests
import time
import json

TOKEN = input("Вставьте TOKEN VK:\n")
ID_VK = int(input("Вставьте ID VK:\n"))
TOKEN_YD = input("Вставьте TOKEN YD:\n")
name_file = input("Введите имя папки, которая будет создана на яндекс диске:\n")


class VKAPICLIENT:
    """ Класс по получению данных из ВК"""
    API_BASE_URL = "https://api.vk.com/method"

    def __init__(self, token, user_id):
        """Хранится токен и id пользователя"""
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        """Хранятся параметры"""
        return {
            'access_token': self.token,
            'v': '5.81'
        }

    def get_photos(self):
        """Получение данных из Вконтакте"""
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1})
        response = requests.get(f'{self.API_BASE_URL}/photos.get', params=params)
        return response.json()

class YDCLIENT:
    """ Класс по обработке данных полученных из ВК и загрузке фото."""
    API_BASE_URL = "https://cloud-api.yandex.net"

    def __init__(self, token):
        """Хранится токен"""
        self.token = token

    def get_common_headers(self):
        """Параметры headers"""
        return {
            'Authorization': self.token,
        }

    def get_common_params(self, name_file):
        """Параметры"""
        return {
            'path': name_file,
        }

    def new_folder(self, name_file):
        """Создание папки ня Яндекс диске"""
        headers = self.get_common_headers()
        params = self.get_common_params(name_file)
        response = requests.put(f'{self.API_BASE_URL}/v1/disk/resources', headers=headers, params=params)
        if 200 <= response.status_code < 300:
            print()
            print(f"Папка {name_file} была создана на яндекс диске.")
        else:
            print()
            print(f"Произошёл сбой")
        return response.status_code

    def get_downloads_photos(self,file_vk):
        """Загрузка фотографий на Яндекс Диск. Сохранение данных в JSON файл."""
        headers = self.get_common_headers()
        params = self.get_common_params(name_file)
        print()
        print(f"В вашем альбоме {file_vk['response']['count']} фотографий. Сколько фотографий загрузить на яндекс диск?")
        photos_items = file_vk['response']['items'][0:int(input())]
        list_foto = []
        likes_list = []
        z = 1
        for i in photos_items:
            time.sleep(0.3)
            if i['likes']['count'] not in likes_list:
                list_foto.append({"file_name": f"{i['likes']['count']}.jpg", "size": i['sizes'][-1]['type']})
                likes_list.append(i['likes']['count'])
                time.sleep(0.3)
                params.update({"path": f"{name_file}/{i['likes']['count']}.jpg",
                               "url": f"{i['sizes'][-1]['url']}"})
                time.sleep(0.3)
                response = requests.post(f'{self.API_BASE_URL}/v1/disk/resources/upload', headers=headers,
                                         params=params)
                time.sleep(0.3)
                if 200 <= response.status_code < 300:
                    print(f"Фотография №{z} загружена.")
                else:
                    print(f"Фотография №{z} НЕ загружена. ПРОИЗОШЁЛ СБОЙ!!!")
                z += 1
                time.sleep(0.3)
            else:
                time.sleep(0.3)
                list_foto.append({"file_name": f"{i['likes']['count']} {datetime.fromtimestamp(i['date']).strftime('%d_%m_%Y')}.jpg", "size": i['sizes'][-1]['type']})
                params.update({"path": f"{name_file}/{i['likes']['count']} {datetime.fromtimestamp(i['date']).strftime('%d_%m_%Y')}.jpg",
                               "url": f"{i['sizes'][-1]['url']}"})
                time.sleep(0.3)
                response = requests.post(f'{self.API_BASE_URL}/v1/disk/resources/upload', headers=headers,
                                         params=params)
                time.sleep(0.3)
                if 200 <= response.status_code < 300:
                    print(f"Фотография №{z} загружена.")
                else:
                    print(f"Фотография №{z} НЕ загружена. ПРОИЗОШЁЛ СБОЙ!!!")
                z += 1
                time.sleep(0.3)
        with open("list_foto.json", "w") as f:
            json.dump(list_foto, f, indent=4)
        print()
        print("JSON-файл создан")
        print()
        print()
        print("Процесс скачивания завершён!!!")


if __name__ == '__main__':
    vk_client = VKAPICLIENT(TOKEN, ID_VK)
    yd_client = YDCLIENT(TOKEN_YD)
    yd_client.new_folder(name_file)
    yd_client.get_downloads_photos(vk_client.get_photos())