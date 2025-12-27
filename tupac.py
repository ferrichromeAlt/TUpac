#!/bin/env python
# -*- coding: utf-8 -*-
"""Create, unpack, and view the contents of ThemePackage files."""

"""!
SPDX-FileCopyrightText: 2025 David Gregory Swindle <david@swindle.net>

SPDX-License-Identifier: GPL-3.0-or-later
"""

# Local imports
from constants import *
from colors import Colors

# Standard Library imports
from sys import argv
import tarfile as tar
import sys, os, locale

# 3rd-party Library Imports
import yaml
lang, encoding = locale.getlocale()

__version__ = '0.1.0'
__author__  = 'David Swindle <david@swindle.net>'

def strip_leading_components(member: tar.TarInfo, count: int) -> tar.TarInfo | None:
    parts = member.name.split('/')
    if count >= len (parts) :
        return None # There's nothing to extract.
    else:
        member.name = '/'.join(parts[count:])
        return member

def main() -> None:
    print(Colors.BOLD, Colors.GREEN, WORDMARK, Colors.END, sep='')
    install_locations = GLOBAL_INSTALL_LOCATIONS if '--global' in argv else LOCAL_INSTALL_LOCATIONS

    # Open the ThemePackage.
    FILENAME = argv[-1] if len (argv) != 1 else ''
    print(Colors.FAINT, 'Extracting package ', FILENAME, '...', Colors.END, sep='')

    if not os.path.exists(FILENAME):
        print(Colors.LIGHT_RED, Colors.BOLD,
                f'{ICONS['error']}\aERROR!\n',
              Colors.END,

              Colors.PURPLE,
                f'You were trying to install a package called “{FILENAME}”,\n',
              Colors.END,

              Colors.RED, Colors.ITALIC,
                "However...\n",
              Colors.END,

              Colors.PURPLE,
                f"TUpac couldn't find any files called “{FILENAME}”.\n",
              Colors.END,
              sep='')
        sys.exit(1)

    try:
        with tar.open(name=FILENAME, mode='r:*') as package:
            REQUIRED_FILES = {
                'themepackage.txt',
                'description.yaml'
            }

            found_themes = set()
            for member in package.getmembers():
                if member.name.split('/')[-1] in install_locations.keys(): found_themes.add(member)

            if len (found_themes) == 0:
                print(Colors.YELLOW, Colors.BOLD,
                        f'{ICONS['warning']}\aWARNING!\n',
                      Colors.END,

                      Colors.YELLOW, Colors.FAINT,
                        f"“{FILENAME}” doesn't contain any themes to be installed.  Because there's nothing to do, TUpac will exit.",
                      Colors.END,

                      Colors.BOLD, Colors.BLUE,
                        f'{ICONS['information']} This is probably an error; you should show this to whoever maintains this package.',
                      Colors.END,
                      sep='')
                sys.exit(0)
            else:
                print(Colors.BLUE,
                        f'{ICONS['information']}Found ',
                      Colors.END,
                      len (found_themes),
                      Colors.BLUE,
                        ' components to install.\n',
                      Colors.END,
                      sep='')

            # Check whether all the files in REQUIRED_FILES are present
            member_names = set(member.name.split('/')[-1] for member in package.getmembers()) # Get of all the names of the package members
            if not member_names.issuperset(REQUIRED_FILES):
                print(Colors.LIGHT_RED, Colors.BOLD,
                        f'{ICONS['error']}\aERROR!\n',
                      Colors.END,

                      Colors.PURPLE,
                        f'You were trying to install a package called “{FILENAME},”\n',
                      Colors.END,

                      Colors.RED, Colors.ITALIC,
                        "However...\n",
                      Colors.END,

                      Colors.PURPLE,
                        f"TUpac can't tell whether “{FILENAME}” is really a ThemePackage because it doesn't have any description files.\n",
                      Colors.END,

                      Colors.BOLD, Colors.BLUE,
                        f'{ICONS['information']}You should show this error to whoever maintains this package.',
                      Colors.END,

                      sep='')
                sys.exit(1)
            else:
                print('Reading package description file...')

                description_file: TarInfo | None = None
                for member in package.getmembers():
                    if member.name.endswith('description.yaml') or member.name.endswith('description.yml'):
                        description_file = member

                description_text = package.extractfile(description_file).read().decode('utf-8')

                if description_text is None:
                    print(Colors.LIGHT_RED, Colors.BOLD,
                        f'{ICONS['error']}\aERROR!\n',
                      Colors.END,

                      Colors.PURPLE,
                        f"TUpac was trying to read “{FILENAME}”'s description file,\n",
                      Colors.END,

                      Colors.RED, Colors.ITALIC,
                        "However...\n",
                      Colors.END,

                      Colors.PURPLE,
                        f"It wasn't a regular file that contained text.\n",
                      Colors.END,

                      Colors.BOLD, Colors.BLUE,
                        f'{ICONS['information']}You should show this error to whoever maintains this package.',
                      Colors.END,

                      sep='')
                    sys.exit(1)

                description_dict = yaml.safe_load(description_text)

                description: ThemePackage
                try:
                    name = description_dict['ThemePackage']['name']
                    author = description_dict['ThemePackage']['author']
                    version = description_dict['ThemePackage']['version']
                    description = ThemePackage(name, author, version)
                except KeyError:
                    print(Colors.LIGHT_RED, Colors.BOLD,
                        f'{ICONS['error']}\aERROR!\n',
                      Colors.END,

                      Colors.PURPLE,
                        f"TUpac was trying to read “{FILENAME}”'s description file,\n",
                      Colors.END,

                      Colors.RED, Colors.ITALIC,
                        "However...\n",
                      Colors.END,

                      Colors.PURPLE,
                        f"Some required information was missing from the description.\n",
                      Colors.END,

                      Colors.BOLD, Colors.BLUE,
                        f'{ICONS['information']}You should show this error to whoever maintains this package.',
                      Colors.END,

                      sep='')
                    sys.exit(1)

                try:
                    description.up_to_date = description_dict['ThemePackage']['up to date']
                    description.description = description_dict['ThemePackage']['description']
                except KeyError:
                    description.up_to_date = description.description = None# No need to raise an error because `up to date` and `description` are optional

            print('====')
            print(Colors.LIGHT_WHITE,
                    'TUpac is ready to install the following packages:\n',
                  Colors.END,
                  Colors.BOLD, Colors.LIGHT_GREEN,
                    description.name + '\n',
                  Colors.END,
                  Colors.LIGHT_GREEN,
                    '\tAuthor: ' + description.author + '\n',
                    '\tVersion: ' + description.version + '\n',
                    '\tDescription: ' + (description.description if description.description is not None else None) + '\n',
                    ('\tUp to date?: ' + ('Yes' if description.up_to_date is True else 'No') + '\n') if description.up_to_date is not None else None,
                  Colors.END,
                  sep='')
            keep_going = input ((Colors.LIGHT_WHITE + Colors.BOLD + '\aContinue? [Y/n] ' + Colors.END))
            if not (keep_going.startswith('y') or keep_going.startswith('Y')):
                print(Colors.RED, Colors.BOLD,
                        'Abort.',
                      Colors.END,
                      sep='')
                sys.exit(0)



            print(Colors.FAINT, "========= BEGIN INSTALLATION ==========", end='\n\n', sep='')

            total_counter = skipped_counter = success_counter = 0
            for theme in found_themes:
                print(f'Extracting “{theme.name}” to “{install_locations[ theme.name.split('/')[-1] ]}”... ', end='')

                try:
                    theme_root_directory = theme.name.rstrip('/') + '/'
                    members = []

                    for member in package.getmembers():
                        if member.name.startswith(theme_root_directory):
                            # Strip the archive root & theme type directory
                            member = strip_leading_components(member, 2)
                            if member is not None: members.append(member)

                    package.extractall( path=install_locations[theme.name.rstrip('/').split('/')[-1]],
                                        members=members )
                    success_counter += 1
                except PermissionError:
                    # TODO: fix
                    print(f"\n{ICONS['warning']}Skipping the installation of an SDDM theme (no permissions)")
                    skipped_counter += 1
                finally:
                    total_counter += 1
                    print(f'Done. ({total_counter}/{len (found_themes)})')

            print(Colors.END, '\n====')
            print(Colors.GREEN, Colors.BOLD,
                f'{ICONS['success']}\aThe ThemePackage {FILENAME} was successfully installed.  Go to System Settings to apply your new themes.\n',
              Colors.END,
                f'\t{Colors.GREEN}{ICONS['success']}: {success_counter}/{total_counter}{Colors.END}\n',
                f'\t{Colors.YELLOW}{Colors.BOLD if skipped_counter > 0 else ''}{ICONS['warning']}: {skipped_counter}/{total_counter}{Colors.END}\n',
              sep='')
    ## This big error chain is for errors that occur when the package is being opened or\
    ## extracted.
    except tar.HeaderError: # This is raised if the tar header is invalid.
        print(f'\aERROR!  {FILENAME} is not a valid ThemePackage.')
        sys.exit(1)
    except tar.CompressionError:
        print(f'\aERROR!  {FILENAME} may be a valid ThemePackage, but it is compressed in'\
            'a way that TUpac cannot understand.  This error should be reported to'\
            'the package maintainers.')
        sys.exit(1)
    except tar.AbsolutePathError:
        print(f'\aERROR!  A member of {FILENAME} uses an absolute path, which is not accepted'\
            'by this program.  This package is likely malware and this error should be'\
            'reported to the maintainers or to the proper authorities.')
        sys.exit(1)
    except tar.SpecialFileError:
        print(f'\aERROR!  A member of {FILENAME} is a special file, which this program does not accept.'\
            'This package is likely malware and this error should be reported to the maintainers or to the proper authorities.')
        sys.exit(1)
    except tar.AbsoluteLinkError:
        print(f'\aERROR!  A member of {FILENAME} is a symbolic link that uses an absolute path,'\
            'which is not accepted by this program.  This package is likely malware and this error'\
            'should be reported to the maintainers or to the proper authorities.')
        sys.exit(1)
    except tar.LinkOutsideDestinationError:
        print(f'\aERROR!  A member of {FILENAME} is a symbolic link that points outside of the'\
            'destination directory.  It is likely either corrupted or someone seriously'\
            'screwed up.')
        sys.exit(1)
    except tar.LinkFallbackError:
        # TODO add error message
        sys.exit(1)


if __name__ == '__main__':
    main()
