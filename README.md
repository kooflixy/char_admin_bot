Создайте новую папку. Вставьте файл characters.json в неё и выполните скрипт ниже

```powershell
git clone https://github.com/kooflixy/char_admin_bot
git clone https://github.com/kooflixy/charbot
copy ./characters.json ./char_admin_bot/
cd ./char_admin_bot/
python create_compose.py
move compose.yml ..
```
