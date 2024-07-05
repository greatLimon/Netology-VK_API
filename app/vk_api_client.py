import requests

class VK_Client:
    _BASE_VK_URL = 'https://api.vk.ru/method/'
    v = '5.199'
    albums = ('wall', 'profile', 'saved')

    def __init__(self, user_id:int, token:str) -> None:
        self.user_id = user_id
        self.token = token

    def _set_common_params(self)->dict:
        return{
            'access_token' : self.token,
            'v' : self.v
        }
    
    def get_photos(self)->list:
        params = self._set_common_params()
        params.update({'owner_id': self.user_id})
        params.update({'album_id' : self.albums[1]})
        params.update({'extended' : 1})

        response = requests.get(self._BASE_VK_URL + 'photos.get', params=params)
        if response.status_code == 200:
            data = response.json()['response']
            if data['count']>0:
                photos = []
                for item in data['items']:
                    biggest_photo = list(filter(lambda s : s['type'] == 'w', item['sizes']))[0]
                    photo = {
                        'url' : biggest_photo['url'],
                        'type' : biggest_photo['type'],
                        'likes' : str(item['likes']['count'])
                    }
                    photos.append(photo)
                return photos
            else:
                return [{'url':'', 'type': '', 'likes':''}]
