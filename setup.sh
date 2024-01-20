#!/bin/sh

# set -e -x

HYPERLAND_CONFIG_DIR="$HOME/.config/hypr"
WAYBAR_CONFIG_DIR="$HOME/.config/waybar"

if [ ! -n "$XDG_CONFIG_HOME" ]; then
  echo "Error: XDG_CONFIG_HOME not set";
  exit 1;
fi

if [ -d "$HYPERLAND_CONFIG_DIR" ] || [ -L "$HYPERLAND_CONFIG_DIR" ]; then
  echo "Error: directory $HYPERLAND_CONFIG_DIR already exist"
  exit 1;
fi

if [ -d "$WAYBAR_CONFIG_DIR" ] || [ -L "$WAYBAR_CONFIG_DIR" ]; then
  echo "Error: directory $WAYBAR_CONFIG_DIR already exist"
  exit 1;
fi

SCRIPT=$(realpath -s "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

ln -s $SCRIPTPATH/hypr $HYPERLAND_CONFIG_DIR || { echo "Error: symlink $HYPERLAND_CONFIG_DIR creation failed"; exit 1; }
ln -s $SCRIPTPATH/waybar $WAYBAR_CONFIG_DIR || { echo "Error: symlink $WAYBAR_CONFIG_DIR creation failed"; exit 1; }

echo "setup complete"
exit 0
