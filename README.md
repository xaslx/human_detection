Приложение python для определения человека в кадре и сохраненияфотографии:

## Установка и запуск


```bash
git clone https://github.com/xaslx/human_detection.git
cd human_detection
poetry install
uvicorn --factory src.main:create_app --reload
```

.env
```env
DB_NAME=photos.db
```
