# This is a script for easier management of special functionality of Lenovo Ideapad Gaming 3 laptop
# Made by Bambuko

import os
import sys
from rich import print
import argparse


class BooleanAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values.lower() in ('yes', 'true', 't', '1'):
            setattr(namespace, self.dest, True)
        elif values.lower() in ('no', 'false', 'f', '0'):
            setattr(namespace, self.dest, False)
        else:
            raise argparse.ArgumentTypeError(f"Unsupported boolean value: {values}")


parser = argparse.ArgumentParser('control.py')
fan_options = parser.add_mutually_exclusive_group()
fan_options.add_argument('--saving', action='store_true', help='Turn on power saving mode of the fans')
fan_options.add_argument('--balanced', action='store_true', help='Turn on balanced mode of the fans')
fan_options.add_argument('--performance', action='store_true', help='Turn on performance mode on the fans')

parser.add_argument('--rapid-charge', type=str, action=BooleanAction, help='Turn on/off rapid charge')
parser.add_argument('--battery-conservation', type=str, action=BooleanAction, help='Turn on/off battery conservation')

args = parser.parse_args()
if not len(sys.argv) > 1:
    exit()

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

# check_conflict()
with open('/proc/acpi/call', 'w') as f:
    if args.rapid_charge:
        if args.battery_conservation:
            print('Cannot set rapid charge and battery conservation at the same time!')
            exit(1)

    with open('/proc/acpi/call', 'w') as f:
        if args.rapid_charge is not None:
            if args.rapid_charge:
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x07')  # Turn on rapid
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x05')  # Turn off conservation
                print('Rapid charge turned on')
            if not args.rapid_charge:
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x08')
                print('Rapid charge turned off')

        if args.battery_conservation is not None:
            if args.battery_conservation:
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x03')  # Turn on conservation
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x08')  # Turn off rapid
                print('Battery conservation turned on')
            if not args.battery_conservation:
                f.write('\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x05')
                print('Battery conservation turned off')
