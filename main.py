#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import os
import sys
from database.db import Database
from ui.login_ui import LoginUI

def main():
    # Initialiser la base de données
    db = Database()
    db.initialize()
    
    # Lancer l'interface utilisateur
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
