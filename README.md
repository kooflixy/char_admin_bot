Создайте новую папку. Вставьте в нее файл characters.json, заполненный по characters.json.example, и выполните скрипт ниже для генерации compose.yml и подгрузки необходимых файлов. 

```powershell
git clone https://github.com/kooflixy/char_admin_bot
git clone https://github.com/kooflixy/charbot
copy ./characters.json ./char_admin_bot/
cd ./char_admin_bot/
python create_compose.py
move compose.yml ..
cd ..
```

После этого да запуска docker-compose просто введите в этой папке команду ниже

```powershell
docker-compose up
```