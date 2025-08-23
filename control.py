# This is a script for easier management of special functionality of Lenovo Ideapad Gaming 3 laptop
# Made by Bambuko

import os
import rich
from rich import print
import argparse


def check_conflict():
    # Check for rapid charge conflicting with battery conservation so both are not enabled at once
    with open('/proc/acpi/call', 'rw') as f:
        f.write('\\_SB.PCI0.LPC0.EC0.QCHO')
        out = f.readall()
        print(out)


parser = argparse.ArgumentParser('Lenovo Ideapad Gaming 3 control utility')
fan_options = parser.add_mutually_exclusive_group()
fan_options.add_argument('--saving', action='store_true', help='Turn on power saving mode of the fans')
fan_options.add_argument('--balanced', action='store_true', help='Turn on balanced mode of the fans')
fan_options.add_argument('--performance', action='store_true', help='Turn on performance mode on the fans')

parser.add_argument('--rapid-charge', help='Turn on/off rapid charge')
parser.add_argument('--battery-conservation', help='Turn on/off battery conservation')

args = parser.parse_args()

with open('/proc/acpi/call', 'w') as f:
    if args.balanced:
        f.write('\\_SB_.GZFD.WMAA 0 0x2C 2')
        print('Switched to balanced mode')
    elif args.performance:
        f.write('\\_SB_.GZFD.WMAA 0 0x2C 3')
        print('Switched to performance Made')
    elif args.saving:
        f.write('\\_SB_.GZFD.WMAA 0 0x2C 1')
        print('Switched to power saving mode')

check_conflict()
