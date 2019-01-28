#!/usr/bin/env python3

from adventure import Adventure
import os

if __name__ == "__main__":
    adventure = Adventure(os.path.dirname(os.path.realpath(__file__)))
    adventure.play()
