#!/usr/bin/env python3
"""
check_duplicates_advanced.py

Finds exact duplicates and fully contained subnets in a target file
compared to a main (reference) file. Supports IPv4 and IPv6.
"""

import ipaddress
import sys
import time
import os


def load_networks_with_lines(filepath, description=""):
    """
    Load networks from a file.
    Returns a list of tuples (original_line, ip_network_object).
    Skips non-CIDR lines silently.
    """
    result = []
    # Count total lines for progress
    total_lines = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for _ in f:
            total_lines += 1

    processed = 0
    last_report = time.time()
    if description:
        print(f"Loading {description}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            processed += 1
            # Show progress every second
            now = time.time()
            if now - last_report >= 1.0:
                percent = (processed / total_lines) * 100
                print(f"\r  Progress: {processed}/{total_lines} ({percent:.1f}%)", end='', flush=True)
                last_report = now

            original = line.rstrip('\n')
            # Remove comments (both ; and #) and strip whitespace
            stripped = original.split(';')[0].split('#')[0].strip()
            if not stripped:
                continue
            try:
                net = ipaddress.ip_network(stripped, strict=False)
                result.append((original, net))
            except ValueError:
                # Not a valid CIDR – skip (do not add)
                pass

    if description:
        print(f"\r  Loaded {len(result)} networks from {description}.")
    return result


def collapse_networks(parsed):
    """
    Collapse a list of networks: keep only those that are not covered by others.
    Input: list of (original_line, ip_network_object)
    Output: collapsed list (minimal covering set)
    """
    if not parsed:
        return []
    # Sort by network address, then by prefix length (wider first)
    parsed.sort(key=lambda x: (x[1].network_address, x[1].prefixlen))
    result = []
    for line, net in parsed:
        # Check if current net is already covered by any network in result
        covered = False
        for _, mnet in result:
            if net.subnet_of(mnet):
                covered = True
                break
        if not covered:
            # Remove from result any networks that are covered by the current one
            new_result = []
            for l, mnet in result:
                if not mnet.subnet_of(net):
                    new_result.append((l, mnet))
            new_result.append((line, net))
            result = new_result
    return result


def find_redundant(target_parsed, main_collapsed):
    """
    Returns a list of original lines from target that are:
      - exact duplicates (same line string) of any main network, or
      - subnets of any main network.
    """
    main_lines = set(line for line, _ in main_collapsed)
    redundant = []
    for line, net in target_parsed:
        # Exact duplicate check
        if line in main_lines:
            redundant.append(line)
            continue
        # Subnet check
        for _, mnet in main_collapsed:
            if net.subnet_of(mnet):
                redundant.append(line)
                break
    return redundant


def process(main_file, target_file, output_removed=None, output_clean=None):
    """
    Main processing function.
    - output_removed: save list of redundant lines to this file
    - output_clean:   save cleaned target file (without redundant lines)
    """
    # Load main (reference) networks
    main_parsed = load_networks_with_lines(main_file, "main file")
    # Split by IP version
    main_v4 = [(l, n) for l, n in main_parsed if n.version == 4]
    main_v6 = [(l, n) for l, n in main_parsed if n.version == 6]
    print(f"Main: {len(main_v4)} IPv4, {len(main_v6)} IPv6")

    # Collapse main networks to minimal covering set
    main_v4_collapsed = collapse_networks(main_v4)
    main_v6_collapsed = collapse_networks(main_v6)
    print(f"Collapsed: {len(main_v4_collapsed)} IPv4, {len(main_v6_collapsed)} IPv6")

    # Load target networks
    target_parsed = load_networks_with_lines(target_file, "target file")
    target_v4 = [(l, n) for l, n in target_parsed if n.version == 4]
    target_v6 = [(l, n) for l, n in target_parsed if n.version == 6]

    # Find redundant lines
    redundant_v4 = find_redundant(target_v4, main_v4_collapsed)
    redundant_v6 = find_redundant(target_v6, main_v6_collapsed)
    redundant = redundant_v4 + redundant_v6

    print(f"\nFound {len(redundant)} redundant lines in target file.\n")

    # Save list of redundant lines if requested
    if output_removed:
        with open(output_removed, 'w', encoding='utf-8') as f:
            for line in redundant:
                f.write(line + '\n')
        print(f"List of lines to remove saved to: {output_removed}")

    # Save cleaned target file if requested
    if output_clean:
        with open(target_file, 'r', encoding='utf-8') as f:
            all_lines = [line.rstrip('\n') for line in f]
        keep_lines = [line for line in all_lines if line not in redundant]
        with open(output_clean, 'w', encoding='utf-8') as f:
            f.write('\n'.join(keep_lines))
            if keep_lines and not keep_lines[-1] == '':
                f.write('\n')
        print(f"Cleaned target file saved to: {output_clean}")

    # If no output files specified, print to console
    if not output_removed and not output_clean:
        print("Lines to remove from target.txt:")
        for line in redundant:
            print(line)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python check_duplicates_advanced.py <main.txt> <target.txt> [--removed removed.txt] [--clean clean.txt]")
        print("  --removed   save list of lines to remove to a file")
        print("  --clean     save cleaned target file (without redundant lines)")
        sys.exit(1)

    main_file = sys.argv[1]
    target_file = sys.argv[2]
    output_removed = None
    output_clean = None

    # Parse command line options
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--removed' and i+1 < len(sys.argv):
            output_removed = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '--clean' and i+1 < len(sys.argv):
            output_clean = sys.argv[i+1]
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}")
            sys.exit(1)

    process(main_file, target_file, output_removed, output_clean)