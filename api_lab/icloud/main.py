from pyicloud import PyiCloudService
from itertools import islice

# логин (пароль и 2FA спросит при запуске)
api = PyiCloudService("ekrivonogov@inbox.ru")

# берём все фото
photos = api.photos.all

# берём первое фото
photo = next(islice(photos, 1))

print("Скачиваем:", photo.filename)

# скачивание (pyicloud возвращает bytes)
data = photo.download()

with open(photo.filename, "wb") as f:
    f.write(data)

print("Готово")
