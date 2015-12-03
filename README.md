FSECplotter2
=============
The interactive plotting application for FSEC.

In current version, compatible with only Shimazu HPLC.

How to install (for OSX users)
----------------
0. Install [homebrew](http://brew.sh/)
1. Execute `brew install python3 qt5 pyqt5`
2. Execute `pip3 install -r requirements.txt`

How to install (for Windows users)
----------------
0. Install python3
1. Execute `pip3 install -r requirements.txt`
2. Install [PyQt5 for windows](https://riverbankcomputing.com/software/pyqt/download5) binary package

Note: At 2015/12/3, PyQt5.5.1 binary package supports only python3.4.


How to use
-----------
0. Start app with `python FSECplotter2.py`
1. Drag and Drop the FSEC logfile(s) to the left-side widget. 
Or, press "Open File" button and select logfiles.
2. Press "Redraw" button.
3. To save figure, press "Save Fig. As..." button to select filename to save. 
PNG, JPG, PDF formats can be selected.
4. "Quick Save" button saves figure as `plot.png` in your home directory.


Test files
------------
This repository includes test files in `test/fixture` directory

+   `test?.txt` :
    test files for large column (GE Healthcare Superose6 increase 10/300)

+   `mini_test?.txt` :
    test files for mini column (GE Healthcare Superdex200 increase 5/150)

Packaging
-----------
Use [Pyinstaller](http://www.pyinstaller.org/), for example:

`pyinstaller --windowed --onefile FSECplotter2.py`