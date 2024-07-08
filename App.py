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
    
    def _read_config(self)->dict:#vk_token, yandex_token, app_status
        with open('config.json', 'r') as config:
            data = json.load(config)
        return data

    def _change_config(self, vk:bool = True, yandex:bool = True)->None:
        if vk:
            vk_token = input('Enter your VK Api token: ')
        else:
            vk_token = self.vk.token
        if yandex:
            ya_token = input('Enter yout Yandex disk Api token: ')
        else:
            ya_token = self.ya.token
        app_status = True
        self._save_config(vk_token, ya_token, app_status)

    def _input_cycle(self,text:str)->bool:
        while True:
            answ = input(text + '[y/n]: ')
            match answ:
                case 'y': return True
                case 'n': return False

    def _print_error(self)->None:
        with open('log.txt', 'r') as log_file:
            error_msg = log_file.read()
        print(error_msg)

    def __init__(self) -> None:
        if not os.path.exists('config.json'):
            self._change_config()
        config = self._read_config()
        if not config['app_status']:
            if self._input_cycle('\nLast time app has crashed. Would you want to change tokens?'):
                self._change_config()
                config = self._read_config()

        user_id = int(input('\nEnter VK user id: '))        
        self.vk = VK_Client(user_id=user_id, token=config['vk_token'])
        self.ya = Yandex_Client(token=config['yandex_token'], user_id=user_id)
        while True:
            self.vk = VK_Client(user_id=user_id, token=config['vk_token'])
            if not self.vk.check_token():
                print('VK has crushed!')
                self._print_error()
                if self._input_cycle('Would you want to change token?'):
                    self._change_config(yandex=False)
                    config = self._read_config()
                else:
                    self.crush()
                    return False
            else:
                break
        while True:
            self.ya = Yandex_Client(token=config['yandex_token'], user_id=user_id)
            if not self.ya.check_folder():
                print('Yandex token has crushed')
                self._print_error()
                if self._input_cycle('Would you want to change token?'):
                    self._change_config(vk=False)
                    config = self._read_config()
                else:
                    self.crush()
                    return False
            else:
                break
        self._save_config(config['vk_token'], config['yandex_token'])
        self.user_id = user_id
    
    def crush(self)->None:
        config = self._read_config()
        self._save_config(config['vk_token'], config['yandex_token'], False)

    def start(self):
        # user_id = 437329788

        if os.path.exists(f'data/{self.user_id}.json'):
            with open(f'data/{self.user_id}.json', 'r') as f:
                exist_photos = json.load(f)
        else:
            exist_photos = {'items' : []}

        photos = self.vk.get_photos()

        for photo in photos:
            path = photo['likes'] + '.png'
            n = 1
            while len(list(filter(lambda x : x['file_name'] == path, exist_photos['items']))) > 0:
                n += 1
                path = f'{photo['likes']}({n}).png'
            if self.ya.save_photo(photo['url'], path):
                print(f'{path} saved to yandex disk')
                exist_photos['items'].append({
                    'file_name' : path,
                    'size' : photo['type']
                })
            else:
                print(f'Error! Photo {path} was not saved!')
        with open(f'data/{self.user_id}.json', 'w') as f:
            json.dump(exist_photos, f)