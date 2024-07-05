import requests

class Yandex_Client:
    _BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token:str, user_id:int) -> None:
        self.token = token
        self.user_id = user_id
        if not self._check_folder():
            print('Ошибка проверки токена Yandex диска!')

    def _set_common_header(self):
        return {
        'Content-Type' : 'application/json',
        'Authorization' : self.token
    }

    def _set_common_params(self):
        return {'path' : f'disk:/Netology-Homework_VK_API/{self.user_id}'}
    
    def _check_folder(self):
        params = self._set_common_params()    
        response = requests.get(self._BASE_URL, headers=self._set_common_header(), params=params)
        if response.status_code == 404:
            path = params['path'].split('/')
            if not self.create_folder_on_yadisk(f'{path[0]}/{path[1]}'):
                return False
            else:
                self.create_folder_on_yadisk(f'{path[0]}/{path[1]}/{path[2]}')
                return True
        elif response.status_code//100 == 2:
            return True
        else:
            return False
    
    def create_folder_on_yadisk(self, path:str)->bool:
        params = {
            'path' : path
        }
        response = requests.put(self._BASE_URL, headers=self._set_common_header(), params=params)
        if response.status_code == 201:
            print(f'Дирректория {path} успешно создана!')
            return True
        else:
            print(f'Ошибка создания папки на Яндекс Диск: {response.status_code}')
            return False

    def save_photo(self, url:str, path:str)->bool:
        header = self._set_common_header()
        params = self._set_common_params()
        params['path'] +=f'/{path}.png'
        params.update({'url' : url})
        response = requests.post(self._BASE_URL+'upload', params=params,headers=header)
        if response.status_code == 202:
            return True
        return False
        