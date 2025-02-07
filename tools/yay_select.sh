#!/bin/bash

# Fetch the list of upgradable AUR packages
packages=$(yay -Qu --aur | awk '{print $1}' | sort)

# Use fzf to interactively select packages (multi-select enabled with Tab key)
selected_packages=$(echo "$packages" | fzf --multi --prompt="Select packages to include: ")

# Check if any packages were selected
if [[ -z "$selected_packages" ]]; then
    echo "No packages selected. Exiting."
    exit 1
fi

# Update only the selected packages
yay -S $selected_packages

