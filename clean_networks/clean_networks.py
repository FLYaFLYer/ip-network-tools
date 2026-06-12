#!/usr/bin/env python3
import ipaddress
import sys
import time
import os
from pathlib import Path

def count_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def load_networks(filepath):
    networks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            try:
                net = ipaddress.ip_network(line, strict=False)
                networks.append(net)
            except ValueError:
                pass
    return networks

def is_subset_or_equal(sub, sup):
    if sub.version != sup.version:
        return False
    return sub.subnet_of(sup)

def get_clean_filename(filename):
    """Формирует имя файла с суффиксом .clean перед расширением."""
    base, ext = os.path.splitext(filename)
    return f"{base}.clean{ext}"

def clean_target_file(main_file, target_file, output_file=None, inplace=False):
    main_nets = load_networks(main_file)
    if not main_nets:
        print("Предупреждение: в основном файле нет корректных CIDR-сетей. Ничего не будет удалено.")
        return

    main_v4 = [n for n in main_nets if n.version == 4]
    main_v6 = [n for n in main_nets if n.version == 6]

    total_lines = count_lines(target_file)
    print(f"Всего строк в файле для очистки: {total_lines}")

    lines_to_keep = []
    removed_count = 0
    total_cidr_lines = 0
    processed = 0
    last_report = time.time()
    report_interval = 1.0

    with open(target_file, 'r', encoding='utf-8') as f:
        for line in f:
            processed += 1
            original_line = line.rstrip('\n')
            stripped = original_line.strip()

            now = time.time()
            if now - last_report >= report_interval:
                percent = (processed / total_lines) * 100
                print(f"\rОбработано строк: {processed} из {total_lines} ({percent:.1f}%) | Удалено: {removed_count}", end='', flush=True)
                last_report = now

            if not stripped or stripped.startswith('#') or stripped.startswith(';'):
                lines_to_keep.append(original_line)
                continue

            try:
                net = ipaddress.ip_network(stripped, strict=False)
                total_cidr_lines += 1
                mains = main_v4 if net.version == 4 else main_v6
                redundant = False
                for main_net in mains:
                    if is_subset_or_equal(net, main_net):
                        redundant = True
                        break
                if redundant:
                    removed_count += 1
                    continue
                else:
                    lines_to_keep.append(original_line)
            except ValueError:
                lines_to_keep.append(original_line)

    print()  # новая строка после прогресса

    if output_file is None and not inplace:
        output_file = get_clean_filename(target_file)
    elif output_file is None and inplace:
        output_file = target_file

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines_to_keep))
        if lines_to_keep and not lines_to_keep[-1] == '':
            f.write('\n')

    print(f"\nГотово. Обработано строк: {processed}")
    print(f"Из них корректных CIDR: {total_cidr_lines}")
    print(f"Удалено (дубли/вложенные): {removed_count}")
    print(f"Результат сохранён в: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Использование: python clean_networks.py <main.txt> <target.txt> [--inplace]")
        print("  --inplace   перезаписать target.txt вместо создания target.clean.txt")
        sys.exit(1)

    main_file = sys.argv[1]
    target_file = sys.argv[2]
    inplace = '--inplace' in sys.argv

    clean_target_file(main_file, target_file, inplace=inplace)