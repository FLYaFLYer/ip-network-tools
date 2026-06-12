# clean_networks.py

[English](#english) | [Русский](#русский)

---

## English

### Description

`clean_networks.py` is a Python script that removes redundant IP network entries from a file. It compares a target list against a reference (main) list and deletes entries that are **exact duplicates** or **subnets** (completely contained within) of any network in the main list.

The script works with both IPv4 and IPv6 CIDR notation. Non-CIDR lines (comments, empty lines, plain text) are preserved.

### Features

- Removes duplicate network entries.
- Removes subnets that are completely inside a larger network from the main list.
- Supports IPv4 and IPv6 (separately, no cross‑version comparison).
- Preserves comments (lines starting with `#` or `;`), empty lines, and non‑CIDR text.
- Shows progress (percentage, lines processed, count removed).
- Outputs result to a file with `.clean` suffix: `target.clean.txt` (or overwrites with `--inplace`).

### Requirements

- Python 3.7 or higher (uses `ipaddress` from standard library).
- No external dependencies.

### Installation

1. Download or copy the script into a file named `clean_networks.py`.
2. Place it in the directory where your list files are located (or add to `PATH`).

### Usage

```bash
python clean_networks.py <main.txt> <target.txt> [--inplace]
```

- `main.txt` – reference file with “already existing” networks.
- `target.txt` – file to be cleaned (will be read, not modified unless `--inplace` is used).
- `--inplace` – overwrite `target.txt` with the cleaned result instead of creating `target.clean.txt`.

### Examples

**main.txt** (reference)
```
# IPv4 main networks
1.0.0.0/24
1.178.4.0/22
192.168.0.0/16

# IPv6 main networks
2001:db8::/32
2600:1f00::/40
```

**target.txt** (to be cleaned)
```
# IPv4 examples
1.178.7.0/24        # will be removed (subnet of 1.178.4.0/22)
192.168.1.0/24      # will be removed (subnet of 192.168.0.0/16)
10.0.0.0/8          # will stay (not in main list)
1.0.0.0/24          # will be removed (exact duplicate)

; IPv6 examples
2001:db8:1::/48     # will be removed (subnet of 2001:db8::/32)
2001:db9::/32       # will stay (not a subnet)

# This non-CIDR line will stay
Just plain text
```

Run:

```bash
python clean_networks.py main.txt target.txt
```

Output file: `target.clean.txt` containing only the lines that are not redundant.

### Notes

- Lines that are not valid CIDR networks (e.g., comments, empty lines, arbitrary text) are **never removed**.
- A subnet is considered redundant if it is fully contained within **any** main network of the same IP version.
- Partial overlaps (e.g., `10.0.0.0/23` and `10.0.2.0/24`) are **not** removed.
- The script does not modify the original `target.txt` unless `--inplace` is specified.
- Progress is shown every second (or every 1000 lines) to indicate that processing is ongoing.

---

## Русский

### Описание

`clean_networks.py` — это скрипт на Python для удаления избыточных записей IP‑сетей из файла. Он сравнивает целевой список с эталонным (основным) и удаляет записи, которые являются **точными дубликатами** или **подсетями** (полностью вложенными) любой сети из основного списка.

Скрипт работает с IPv4 и IPv6 в нотации CIDR. Строки, не являющиеся корректными CIDR (комментарии, пустые строки, произвольный текст), сохраняются без изменений.

### Возможности

- Удаляет точные дубликаты сетей.
- Удаляет подсети, полностью вложенные в более крупные сети из основного списка.
- Поддерживает IPv4 и IPv6 (сравнение только в пределах одной версии).
- Сохраняет комментарии (строки, начинающиеся с `#` или `;`), пустые строки и текст, не являющийся CIDR.
- Показывает прогресс выполнения (проценты, количество обработанных строк, число удалённых записей).
- Сохраняет результат в файл с суффиксом `.clean`: `target.clean.txt` (или перезаписывает исходный с флагом `--inplace`).

### Требования

- Python 3.7 или выше (используется модуль `ipaddress` из стандартной библиотеки).
- Дополнительных зависимостей не требуется.

### Установка

1. Скачайте или скопируйте скрипт в файл с именем `clean_networks.py`.
2. Поместите его в каталог с вашими списками или добавьте в `PATH`.

### Использование

```bash
python clean_networks.py <main.txt> <target.txt> [--inplace]
```

- `main.txt` – эталонный файл с «уже существующими» сетями.
- `target.txt` – файл для очистки (будет прочитан, но не изменён, если не указан `--inplace`).
- `--inplace` – перезаписать `target.txt` очищенным результатом вместо создания `target.clean.txt`.

### Примеры

**main.txt** (эталон)
```
# Основные IPv4 сети
1.0.0.0/24
1.178.4.0/22
192.168.0.0/16

# Основные IPv6 сети
2001:db8::/32
2600:1f00::/40
```

**target.txt** (очищаемый)
```
# Примеры IPv4
1.178.7.0/24        # будет удалена (подсеть 1.178.4.0/22)
192.168.1.0/24      # будет удалена (подсеть 192.168.0.0/16)
10.0.0.0/8          # останется (нет в main)
1.0.0.0/24          # будет удалена (точный дубликат)

; Примеры IPv6
2001:db8:1::/48     # будет удалена (подсеть 2001:db8::/32)
2001:db9::/32       # останется (не подсеть)

# Эта строка не CIDR – останется
Обычный текст
```

Запуск:

```bash
python clean_networks.py main.txt target.txt
```

Выходной файл: `target.clean.txt`, содержащий только строки, которые не являются избыточными.

### Примечания

- Строки, не являющиеся валидными CIDR-сетями (комментарии, пустые строки, произвольный текст), **никогда не удаляются**.
- Подсеть считается избыточной, если она полностью вложена в **любую** основную сеть той же версии IP.
- Частичные пересечения (например, `10.0.0.0/23` и `10.0.2.0/24`) **не удаляются**.
- Скрипт не изменяет исходный `target.txt`, если не указан флаг `--inplace`.
- Прогресс выводится каждую секунду (или каждые 1000 строк), чтобы вы видели, что обработка продолжается.