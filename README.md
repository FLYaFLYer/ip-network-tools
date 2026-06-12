# IP Network Tools

[English](#english) | [Русский](#русский)

---

## English

This repository contains two Python tools for managing IP network lists (IPv4/IPv6 in CIDR notation):

1. **[check_duplicates](./check_duplicates)** – Finds exact duplicates and fully contained subnets between a reference list and a target list.
2. **[clean_networks](./clean_networks)** – Removes redundant networks (duplicates or subnets) from a target file based on a reference list.

Both tools support IPv4 and IPv6, preserve comments and non‑CIDR lines, and show progress for large files.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/FLYaFLYer/ip-network-tools.git
cd ip-network-tools

# Check for duplicates (output cleaned file)
python check_duplicates/check_duplicates_advanced.py main.txt target.txt --clean target.clean.txt

# Clean a network list (output cleaned file)
python clean_networks/clean_networks.py main.txt target.txt --clean target.clean.txt
```

### Requirements

- Python 3.7 or higher (uses only the standard library, no external dependencies)

### Documentation

See the individual README files inside each subfolder for detailed usage, examples, and command-line options.

### License

[MIT License](./LICENSE) © 2026 FLYaFLYer

---

## Русский

Этот репозиторий содержит два инструмента на Python для работы со списками IP-сетей (IPv4/IPv6 в нотации CIDR):

1. **[check_duplicates](./check_duplicates)** – Находит точные дубликаты и полностью вложенные подсети между эталонным списком и целевым.
2. **[clean_networks](./clean_networks)** – Удаляет избыточные сети (дубликаты или вложенные) из целевого файла на основе эталонного списка.

Оба инструмента поддерживают IPv4 и IPv6, сохраняют комментарии и строки без CIDR, показывают прогресс для больших файлов.

### Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/FLYaFLYer/ip-network-tools.git
cd ip-network-tools

# Проверить на дубликаты (создать очищенный файл)
python check_duplicates/check_duplicates_advanced.py main.txt target.txt --clean target.clean.txt

# Очистить список сетей (создать очищенный файл)
python clean_networks/clean_networks.py main.txt target.txt --clean target.clean.txt
```

### Требования

- Python 3.7 или выше (используется только стандартная библиотека, внешних зависимостей нет)

### Документация

Подробное описание и примеры использования в файлах README внутри каждой подпапки.

### Лицензия

[MIT License](./LICENSE) © 2026 FLYaFLYer

---