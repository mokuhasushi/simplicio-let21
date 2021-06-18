# Sto provando a impostare la struttura del progetto come suggerito in
# https://docs.python-guide.org/writing/structure/

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "simplicio")))

import shuntingyard
import exceptions
import semplificatore
