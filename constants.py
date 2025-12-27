#!/bin/env python
# -*- coding: utf-8 -*-
""":mod:`constants.py`: Constants and classes used by TUpac."""
"""!
SPDX-FileCopyrightText: 2025 David Gregory Swindle <david@swindle.net>

SPDX-License-Identifier: GPL-3.0-or-later
"""

import os
from sys import argv
import locale
from dataclasses import dataclass
from datetime import date

lang, encoding = locale.getlocale()

GLOBAL_INSTALL_LOCATIONS = {
    'global themes':            '/usr/share/plasma/look-and-feel/',
    'plasma styles':            '/usr/share/plasma/desktoptheme/',
    'color schemes':            '/usr/share/color-schemes/',
    'icon themes':              '/usr/share/icons/',
    'panel layout templates':   '/usr/share/plasma/layout-templates/',
    'task switchers':           '/usr/share/kwin/tabbox/',
    'plasma widgets':           '/usr/share/plasma/plasmoids/', # AKA Plasmoids
    'wallpaper plugins':        '/usr/share/plasma/wallpapers/',
    'window decorations':       '/usr/share/aurorae/themes/',
    'kwin effects':             '/usr/share/kwin/effects/', # AKA Desktop Effects
    'kwin scripts':             '/usr/share/kwin/scripts/',
    'sddm themes':              '/usr/share/sddm/themes/', # AKA Login Themes/Screens
    'cursor themes':            '/usr/share/icons/'
}
LOCAL_INSTALL_LOCATIONS = {
    'global themes':            os.path.expanduser('~/.local/share/plasma/look-and-feel/'),
    'plasma styles':            os.path.expanduser('~/.local/share/plasma/desktoptheme/'),
    'color schemes':            os.path.expanduser('~/.local/share/color-schemes/'),
    'icon themes':              (os.path.expanduser('~/.local/share/icons/') if '--oldcursor' not in argv else os.path.expanduser('~/.icons/')),
    'panel layout templates':   os.path.expanduser('~/.local/share/plasma/layout-templates/'),
    'task switchers':           os.path.expanduser('~/.local/share/kwin/tabbox/'),
    'plasma widgets':           os.path.expanduser('~/.local/share/plasma/plasmoids/'), # AKA Plasmoids
    'wallpaper plugins':        os.path.expanduser('~/.local/share/plasma/wallpapers/'),
    'window decorations':       os.path.expanduser('~/.local/share/aurorae/themes/'),
    'kwin effects':             os.path.expanduser('~/.local/share/kwin/effects/'), # AKA Desktop Effects
    'kwin scripts':             os.path.expanduser('~/.local/share/kwin/scripts/'),
    'sddm themes':              os.path.expanduser('/usr/share/sddm/themes/'), # AKA Login Themes/Screens
    'cursor themes':            (os.path.expanduser('~/.local/share/icons/') if '--oldcursor' not in argv else os.path.expanduser('~/.icons')),
    'kvantum themes':           os.path.expanduser('~/.config/Kvantum/')
}
EMOJI_ICONS = {
    'error': '✔️' if lang == 'ja' or lang == 'jpn' else '❌', # In Japan, a check mark ✔️ means "no" or "wrong" and an O-mark ⭕️ means "yes", "correct", or "good".
    'warning': '⚠️',
    'success': '⭕️' if lang == 'ja' or lang == 'jpn' else '✅',
    'information': 'ℹ️'
}
NERD_FONT_ICONS = {
    'error': ' ',
    'warning': ' ',
    'success': ' ',
    'information': ' '
}
ICONS = EMOJI_ICONS if not os.getenv('NERD_FONT') else NERD_FONT_ICONS

try:
    wordmarkDOTtxt = open('wordmark.txt').read()
    # Strip comment lines from wordmark file
    WORDMARK = ''
    for line in wordmarkDOTtxt.split('\n'):
        if not line.startswith('#'): WORDMARK += (line + '\n')
except FileNotFoundError:
    WORDMARK = r"""
   ________  __                    ____   ___  ____
  /_  __/ / / /___  ____ _,____   / __ \ <  / / __ \
   / / / / / / _  \/ __ `/ ___/  /  \/ / / / /  \/ /
  / / / /_/ / /_) / (_/ / (__   / /\  / / /_/ /\  /
 /_/  \____/ ,___/\__,_/\___/   \____(_)_/(_)____/
          /_/        Theme Unpacker Version 0.1.0
"""

@dataclass
class ThemePackage:
    """Class for storing the description of a ThemePackage."""
    name: str
    author: str
    version: str | int
    credits: list[str] | None = None
    pub_date: date | None = None
    up_to_date: bool | None = None
    description: str | None = None
