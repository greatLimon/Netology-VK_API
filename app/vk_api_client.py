import requests

class VK_Client:
    _BASE_VK_URL = 'https://api.vk.ru/method/'
    v = '5.199'
    albums = ('wall', 'profile', 'saved')

    def check_token(self)->bool:
        params = self._set_common_params()
        response = requests.get(self._BASE_VK_URL + 'photos.get', params=params)
        data = response.json()
        if data.get('error'):
            with open('log.txt', 'w') as log_file:
                log_file.write(data['error']['error_msg'])
            return False
        else: return True

    def __init__(self, user_id:int, token:str) -> None:
        self.user_id = user_id
        self.token = token

    def _set_common_params(self)->dict:
        return{
            'access_token' : self.token,
            'v' : self.v,
            'owner_id': self.user_id,
            'album_id' : self.albums[1],
            'extended' : 1,
            'photo_sizes' : 1
        }
    
    def _get_biggest_photo(self, item:dict)->dict:
        sizes_list = ['w','z','y','r','q','p','o','x','m','s']
        for size_type in sizes_list:
            photo = list(filter(lambda s : s['type'] == size_type, item))
            if len(photo) > 0:
                return photo[0]
            
    def get_photos(self)->list:
        params = self._set_common_params()
        response = requests.get(self._BASE_VK_URL + 'photos.get', params=params)
        if response.status_code == 200:
            data = response.json()['response']
            if data['count']>0:
                photos = []
                for item in data['items']:
                    biggest_photo = self._get_biggest_photo(item['sizes'])
                    photo = {
                        'url' : biggest_photo['url'],
                        'type' : biggest_photo['type'],
                        'likes' : str(item['likes']['count'])
                    }
                    photos.append(photo)
                return photos
            else:
                if data.get('error'):
                    with open('log.txt', 'w') as log_file:
                        log_file.write(data['error']['error_msg'])
                return False
                # return [{'url':'', 'type': '', 'likes':''}]
