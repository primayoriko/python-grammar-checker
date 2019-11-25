# Ini untuk Parser #
# Kelompok : The Godfather #
# 1. Jun Ho Choi Hedyatmo / 13518044
# 2. Naufal Prima Yoriko / 13518146
# 3. Stefanus Gusega Gunawan / 13518149
import sys
import os
import re
import pandas as pd

class Parser:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.raw_code = file.read()
            self.code = self.raw_code.splitlines()
    
