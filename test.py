#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse
parser = argparse.ArgumentParser()


subparsers = parser.add_subparsers(title="actions", dest="action")
change = subparsers.add_parser("change")
changesub = change.add_subparsers(title="changes", dest="change")
change_quire = changesub.add_parser("quire")
change_quire.add_argument("echo")

args = parser.parse_args()
print args.__dict__
