#!/usr/bin/env python3
import yaml
import os

# Load the already welcomed persons from a state file
welcomed_persons_file = "welcomed_persons.txt"
welcomed_persons = set()

if os.path.exists(welcomed_persons_file):
    with open(welcomed_persons_file, "r") as file:
        welcomed_persons = set(line.strip() for line in file)

# Load personas from personas.yml
with open("personas.yml", "r") as file:
    data = yaml.safe_load(file)

new_welcomed_persons = []

# Iterate through each person and greet if they haven’t been welcomed yet
for person_key, person_info in data["people"].items():
    name = person_info["name"]

    if name in welcomed_persons:
        print(f"Person {name} is already welcomed.")
    else:
        print(f"Hello to SAP, {name}")
        new_welcomed_persons.append(name)
        welcomed_persons.add(name)

# Save new welcomed persons to the state file
if new_welcomed_persons:
    with open(welcomed_persons_file, "a") as file:
        for name in new_welcomed_persons:
            file.write(f"{name}\n")
