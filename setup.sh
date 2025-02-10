#!/bin/sh
# set -e -x

HYPERLAND_CONFIG_DIR="$HOME/.config/hypr"
WAYBAR_CONFIG_DIR="$HOME/.config/waybar"

SCRIPT=$(realpath -s "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
HYPR_SHARED_PLATFORM_CONF="empty"

if [ ! -n "$XDG_CONFIG_HOME" ]; then
  echo "Error: XDG_CONFIG_HOME not set";
  exit 1;
fi

if [ "$1" == "--desktop" ]; then
  HYPR_SHARED_PLATFORM_CONF="$SCRIPTPATH/hypr/desktop.conf"
fi

if [ "$1" == "--laptop" ]; then
  HYPR_SHARED_PLATFORM_CONF="$SCRIPTPATH/hypr/laptop.conf"
fi

if [ "$HYPR_SHARED_PLATFORM_CONF" == "empty" ]; then
  echo "Platform config not set, available options: --desktop --laptop"
  exit -1
fi

ln -s "$HYPR_SHARED_PLATFORM_CONF" "$SCRIPTPATH/hypr/shared.conf" || { echo "Warn: symlink $SCRIPTPATH/hypr/shared.conf already exist"; }

if [ -d "$HYPERLAND_CONFIG_DIR" ] || [ -L "$HYPERLAND_CONFIG_DIR" ]; then
  echo "Warn: directory $HYPERLAND_CONFIG_DIR already exist; not copying config"
else
  ln -s $SCRIPTPATH/hypr $HYPERLAND_CONFIG_DIR || { echo "Error: symlink $HYPERLAND_CONFIG_DIR creation failed"; exit 1; }
fi

if [ -d "$WAYBAR_CONFIG_DIR" ] || [ -L "$WAYBAR_CONFIG_DIR" ]; then
  echo "Warn: directory $WAYBAR_CONFIG_DIR already exist; not copying config"
else
  ln -s $SCRIPTPATH/waybar $WAYBAR_CONFIG_DIR || { echo "Error: symlink $WAYBAR_CONFIG_DIR creation failed"; exit 1; }
fi

echo "setup complete"
exit 0
