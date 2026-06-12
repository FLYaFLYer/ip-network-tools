# check_duplicates_advanced.py

[English](#english) | [Русский](#русский)

---

## English

### Description

`check_duplicates_advanced.py` is a Python script that finds **exact duplicate lines** and **fully contained subnets** in a target file by comparing it with a reference (main) file. It supports both IPv4 and IPv6 CIDR notation.

The script is useful for cleaning IP allowlists, blocklists, or any list of network prefixes where you want to remove entries already covered by larger networks in another file.

### Features

- Detects exact duplicate lines (identical strings) between main and target.
- Detects subnets that are completely inside any network from the main file.
- Separate handling of IPv4 and IPv6 (no cross‑version comparison).
- Preserves comments, empty lines, and non‑CIDR lines (they are never removed).
- Collapses the main network list to minimal coverage for faster checks.
- Progress indicator for large files (updates every second).
- Output options:
  - Print redundant lines to console.
  - Save list of redundant lines to a file (`--removed`).
  - Generate a cleaned version of the target file (`--clean`).

### Requirements

- Python 3.7 or higher (uses `ipaddress` from standard library).
- No external dependencies.

### Installation

1. Download or copy the script into a file named `check_duplicates_advanced.py`.
2. Place it in the directory with your list files (or add to `PATH`).

### Usage

```bash
python check_duplicates_advanced.py <main.txt> <target.txt> [--removed removed.txt] [--clean clean.txt]
```

- `main.txt` – reference file with “already existing” networks.
- `target.txt` – file to be checked for duplicates/subnets.
- `--removed` – (optional) save the list of redundant lines to the specified file.
- `--clean` – (optional) create a cleaned version of `target.txt` without redundant lines.

### Examples

#### Example files

**main.txt** (reference)
```
# Main reference networks (IPv4 & IPv6)
# IPv4
1.0.0.0/24
1.178.4.0/22
192.168.0.0/16

# IPv6
2001:db8::/32
2600:1f00::/40
```

**target.txt** (to be checked)
```
# Target file to check
# IPv4 examples
1.178.7.0/24          # will be removed (subnet of 1.178.4.0/22)
1.178.8.0/24          # will be removed (subnet of 1.178.4.0/22)
192.168.1.0/24        # will be removed (subnet of 192.168.0.0/16)
10.0.0.0/8            # will stay
1.0.0.0/24            # will be removed (exact duplicate)
8.8.8.0/24            # will stay

; IPv6 examples
2001:db8:1::/48       # will be removed (subnet of 2001:db8::/32)
2001:db9::/32         # will stay
2600:1f00:1000::/48   # will be removed (subnet of 2600:1f00::/40)
2600:1f01::/40        # will stay

# Non-CIDR lines are always kept
This is just plain text
```

#### Commands

1. **Print redundant lines to console**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt
   ```
   Output:
   ```
   Loading main file...
   ...
   Found 6 redundant lines in target file.

   Lines to remove from target.txt:
   1.178.7.0/24
   1.178.8.0/24
   192.168.1.0/24
   1.0.0.0/24
   2001:db8:1::/48
   2600:1f00:1000::/48
   ```

2. **Save redundant lines to a file**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --removed to_remove.txt
   ```

3. **Create cleaned target file**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --clean target.clean.txt
   ```
   The cleaned file will contain all lines except the redundant ones.

4. **Both at once**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --removed to_remove.txt --clean target.clean.txt
   ```

### Important Notes

- Only **exact string matches** and **full subnet containment** are considered redundant.
- Partial overlaps (e.g., `10.0.0.0/23` and `10.0.2.0/24`) are **not** removed.
- Comments (lines starting with `#` or `;`), empty lines, and non‑CIDR text are **never removed**.
- The script does **not** modify the original `target.txt` unless you use `--clean` with the same filename (not recommended). Use `--clean target.clean.txt` to keep the original unchanged.
- For large files, progress is shown automatically (every second).

---

## Русский

### Описание

`check_duplicates_advanced.py` — это скрипт на Python для поиска **точных дубликатов строк** и **полностью вложенных подсетей** в целевом файле по сравнению с эталонным. Поддерживает IPv4 и IPv6 в нотации CIDR.

Скрипт полезен для очистки списков разрешённых/заблокированных IP, а также любых списков сетей, где нужно убрать записи, уже покрытые более крупными сетями из другого файла.

### Возможности

- Находит точные дубликаты строк между основным и целевым файлом.
- Находит подсети, полностью вложенные в любую сеть из основного файла.
- Раздельная обработка IPv4 и IPv6 (сравнение только в пределах одной версии).
- Сохраняет комментарии, пустые строки и текст, не являющийся CIDR (они никогда не удаляются).
- Сжимает основной список до минимального покрытия для ускорения проверки.
- Индикатор прогресса для больших файлов (обновление каждую секунду).
- Режимы вывода:
  - Вывод избыточных строк в консоль.
  - Сохранение списка избыточных строк в файл (`--removed`).
  - Создание очищенной версии целевого файла (`--clean`).

### Требования

- Python 3.7 или выше (используется модуль `ipaddress` из стандартной библиотеки).
- Дополнительных зависимостей не требуется.

### Установка

1. Скачайте или скопируйте скрипт в файл с именем `check_duplicates_advanced.py`.
2. Поместите его в каталог с вашими файлами списков (или добавьте в `PATH`).

### Использование

```bash
python check_duplicates_advanced.py <main.txt> <target.txt> [--removed removed.txt] [--clean clean.txt]
```

- `main.txt` – эталонный файл с «уже существующими» сетями.
- `target.txt` – файл для проверки на дубликаты/вложенные сети.
- `--removed` – (опционально) сохранить список избыточных строк в указанный файл.
- `--clean` – (опционально) создать очищенную версию `target.txt` без избыточных строк.

### Примеры

#### Примеры файлов

**main.txt** (эталон)
```
# Основные сети (IPv4 и IPv6)
# IPv4
1.0.0.0/24
1.178.4.0/22
192.168.0.0/16

# IPv6
2001:db8::/32
2600:1f00::/40
```

**target.txt** (проверяемый)
```
# Целевой файл для проверки
# Примеры IPv4
1.178.7.0/24          # будет удалена (подсеть 1.178.4.0/22)
1.178.8.0/24          # будет удалена (подсеть 1.178.4.0/22)
192.168.1.0/24        # будет удалена (подсеть 192.168.0.0/16)
10.0.0.0/8            # останется
1.0.0.0/24            # будет удалена (точный дубликат)
8.8.8.0/24            # останется

; Примеры IPv6
2001:db8:1::/48       # будет удалена (подсеть 2001:db8::/32)
2001:db9::/32         # останется
2600:1f00:1000::/48   # будет удалена (подсеть 2600:1f00::/40)
2600:1f01::/40        # останется

# Не-CIDR строки всегда сохраняются
Это просто обычный текст
```

#### Команды

1. **Вывести избыточные строки в консоль**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt
   ```
   Вывод:
   ```
   Loading main file...
   ...
   Found 6 redundant lines in target file.

   Lines to remove from target.txt:
   1.178.7.0/24
   1.178.8.0/24
   192.168.1.0/24
   1.0.0.0/24
   2001:db8:1::/48
   2600:1f00:1000::/48
   ```

2. **Сохранить список избыточных строк в файл**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --removed to_remove.txt
   ```

3. **Создать очищенную версию целевого файла**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --clean target.clean.txt
   ```
   Очищенный файл будет содержать все строки, кроме избыточных.

4. **Оба действия сразу**  
   ```bash
   python check_duplicates_advanced.py main.txt target.txt --removed to_remove.txt --clean target.clean.txt
   ```

### Важные замечания

- Избыточными считаются только **точные совпадения строк** и **полная вложенность подсетей**.
- Частичные пересечения (например, `10.0.0.0/23` и `10.0.2.0/24`) **не удаляются**.
- Комментарии (строки, начинающиеся с `#` или `;`), пустые строки и текст, не являющийся CIDR, **никогда не удаляются**.
- Скрипт **не изменяет** исходный `target.txt`, если только вы не используете `--clean` с тем же именем (не рекомендуется). Используйте `--clean target.clean.txt`, чтобы сохранить оригинал.
- Для больших файлов прогресс отображается автоматически (каждую секунду).