# 41mo Hyperland config scripts

## Setup
clone this repo in some directory:

```bash 
git clone https://github.com/41Mo/hyprconfig.git
cd hyprconfig
```

bootstrap it:

```
./setup.sh
```

from this point you may start ricing your config simply inside hyprconfig directory.

## Dependecies

- wofi as an application launcher.
- alacritty as an terminal emulator.
- dolphin as an file manager.
- brillo as an brightness manager.
- waybar as an status bar.
- dunst as an notification daemon.
- pipewire + wireplumber as an audio stack.
- xdg-desktop-portal-hyprland as an portal.
- polkit-kde-agent as an auth agent.
- cliphist as an cipboard manager (wl-clipboard).

## Useful tools
to configure qt and gtk themes
- qt5ct for QT apps.
- nwg-look for GTK apps.

## Tips: Hacks and fixes
### Chromium browsers persistent wayland configuration
Go to chrome://flags

Search "Preferred Ozone platform"

Set it to "Wayland"

Restart
Go to chrome://flags

Search "Preferred Ozone platform"

Set it to "Wayland"

Restart

### Dolphin customization
Setup preffeted terminal and background color
in /.config/kdeglobals
```
[General]
TerminalApplication=alacritty -e tmux new

[Colors:View]
BackgroundNormal=#2E2E2E
```

### Disable KdeWallet
it asks for keyring on each browser opening

add in ~/.config/kwalletrc
```
[wallet]
enabled=false
first use=false
```

## Archlinux quick dependecies install

must have dependecies
```bash
yay -Syu --repo
cat arch.packages | yay -S -
```

optional
```bash
cat optional_arch.packages  | yay -S -
```

