# PutlerKiller-II
Декілька скриншнотів з гри:

![изображение](https://github.com/makarasty/PutlerKiller-II/assets/71918286/dec573b5-c666-4833-a11a-54d5a9f5262b)

![изображение](https://github.com/makarasty/PutlerKiller-II/assets/71918286/2232319e-d2bd-49fd-87c2-77c8561e8950)

![изображение](https://github.com/makarasty/PutlerKiller-II/assets/71918286/e73e2d32-98fe-4d83-8863-dc9c36aab00a)

# Requirements
Для встановлення гри потрібно:
- Встановити [git](https://git-scm.com/downloads),
- Встановити [Python](https://www.python.org/downloads/),
- `git clone https://github.com/makarasty/PutlerKiller-II`
- `cd PutlerKiller-II`
- `pip install -r requirements.txt`
- `python main.py`

# Compile
`pyinstaller --noconfirm --onefile --windowed --icon ".\PutlerKiller-II\src\putler-3.ico" --name "PutlerKillerII" --add-data ".\PutlerKiller-II\налаштування.py;." --add-data ".\PutlerKiller-II\src;src/"  ".\PutlerKiller-II\main.py"`

# Download
[PutlerKillerII.exe](https://github.com/makarasty/PutlerKiller-II/releases/latest)
