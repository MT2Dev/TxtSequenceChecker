#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import Dict, List, Set

#################################################################
## Author:        MT2Dev       -      25/10/2024               ##
## Environment:   Python 2.7 (FreeBSD/Windows)                 ##
## USAGE SYNTAX:  python txt_checker.py mob_drop_item.txt      ##
#################################################################

def check_sequence_gaps(filename: str) -> Dict[str, List[int]]:
	current_group = ""
	groups: Dict[str, Set[int]] = {}
	inside_group = False
	with open(filename, 'r') as file:
		for line in file:
			line = line.strip()
			if line.startswith('Group'):
				current_group = line.split()[1]
				groups[current_group] = set()
				inside_group = True
				continue
			if line == '}':
				inside_group = False
				continue
			if inside_group and line and line[0].isdigit():
				try:
					sequence_number = int(line.split()[0])
					groups[current_group].add(sequence_number)
				except (IndexError, ValueError):
					continue
	#print("\nDebug - Found numbers in each group:")
	for group_name, numbers in groups.items():
		print(f"{group_name}: {sorted(numbers)}")
	gaps: Dict[str, List[int]] = {}

	for group_name, numbers in groups.items():
		if not numbers:
			continue
		max_num = max(numbers)
		missing = sorted([num for num in range(1, max_num + 1) if num not in numbers])
		if missing:
			gaps[group_name] = missing
	return gaps

def format_results(gaps: Dict[str, List[int]]) -> str:
	if not gaps:
		return "No sequence gaps found in any group."
	result = []
	result.append("Groups with sequence gaps:")
	for group_name, missing_numbers in sorted(gaps.items()):
		missing_str = ", ".join(str(x) for x in missing_numbers)
		result.append(f"\nGroup: {group_name}")
		result.append(f"Missing Numbers: {missing_str}")
	return "\n".join(result)

def main():
	import sys
	if len(sys.argv) != 2:
		print("Usage: python txt_checker.py xxx.txt")
		sys.exit(1)
	filename = sys.argv[1]
	try:
		gaps = check_sequence_gaps(filename)
		print(format_results(gaps))
	except FileNotFoundError:
		print(f"Error: File '{filename}' not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	main()

