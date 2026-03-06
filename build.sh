pyinstaller main.py \                                                                                                                                                  ─╯
          --name Backstaff \
          --onefile \
          --noconfirm \
          --clean \
          --add-data "Reinforcement:Reinforcement" \
          --hidden-import PyQt5.sip