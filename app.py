#!/usr/bin/env python

from classes.adventure import Adventure
import os

if __name__ == "__main__":
    adventure = Adventure(os.path.dirname(os.path.realpath(__file__)))
    adventure.play()
