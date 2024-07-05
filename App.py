import os
import json

from app.vk_api_client import VK_Client
from app.yandex_api_client import Yandex_Client

class App:
    def _save_config(self,vk_token:str = '', ya_token:str = '', app_status:bool = True)->None:
        with open('config.json', 'w') as config:
            json.dump({
                'vk_token' : vk_token,
                'yandex_token' : ya_token,
                'app_status' : app_status
            }, config)
    
    def _change_config(self)->None:
        vk_token = input('Enter your VK Api token: ')
        ya_token = input('Enter yout Yandex disk Api token: ')
        app_status = True
        self._save_config(vk_token, ya_token, app_status)

    def __init__(self) -> None:
        if not os.path.exists('config.json'):
            self._change_config()
        with open('config.json', 'r') as config:
            data = json.load(config)
        vk_token = data['vk_token']
        ya_token = data['yandex_token']
        app_status = data['app_status']
        if not app_status:
            while True:
                answ = input('Last time app has crashed. Would you want to change tokens? [y/n]')
                if answ == 'y':
                    self._change_config()
                if answ == 'n':
                    break
                
        self.vk_token = vk_token
        self.ya_token = ya_token
        self.app_status = app_status
        self.user_id = int(input('Enter VK user id: '))
    
    def bug(self)->None:
        self._save_config(self.vk_token, self.ya_token, False)

    def start(self):
        # user_id = 437329788
        vk = VK_Client(self.user_id, self.vk_token)
        yd = Yandex_Client(self.ya_token, self.user_id)
        if os.path.exists(f'data/{self.user_id}.json'):
            with open(f'data/{self.user_id}.json', 'r') as f:
                exist_photos = json.load(f)
        else:
            exist_photos = {'items' : []}

        photos = vk.get_photos()

        for photo in photos:
            path = photo['likes'] + '.png'
            n = 1
            while len(list(filter(lambda x : x['file_name'] == path, exist_photos['items']))) > 0:
                n += 1
                path = f'{photo['likes']}({n}).png'
            if yd.save_photo(photo['url'], path):
                print(f'{path} saved to yandex disk')
                exist_photos['items'].append({
                    'file_name' : path,
                    'size' : photo['type']
                })
            else:
                print(f'Error! Photo {path} was not saved!')
        with open(f'data/{self.user_id}.json', 'w') as f:
            json.dump(exist_photos, f)