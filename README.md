FSECplotter2
=============
The interactive plotting application for FSEC.

In current version, compatible with Shimadzu HPLC and Hitachi HPLC formats.

Features
--------------
+ A simple GUI based control for drawing Shimadzu and Hitachi (or other HPLCs) format chromatograms.
+ Drag&Drop operation for file opening.
+ Cross platform application with python3 and PyQt5.
+ Drawing melting curve in the FSEC-TS assay (Tools->calcTm).
+ Normalizing Y-axis (Tools->Y-axis scaling).
+ Peak integration (Tools->Peak integration).
+ Max peak table (Tools->Peak table).
+ The line color and line width can be changed manually.
+ The unit of X-axis can be selected from [Time(min)] and [Volume(mL)]
+ The style and context setting in the [seaborn package](https://stanford.edu/~mwaskom/software/seaborn/index.html) is supported.
Check "use seaborn package" in the Preference->Figure Canvas Setting, and select the style and context.
This setting was enabled when the app is restarted.
+ The csv data table (long format) can be exported.
+ You can extend the file parser with your own parser for another HPLC file (See below).


How to download package (only for Windows or MacOSX)
------------------------------------------------------
0. Download appropriate package from [releases tab](https://github.com/TaizoAyase/FSECplotter2/releases)
1. Double click the downloaded

If you cannot launch from downloaded package, please try to launch from source code (below).


How to launch from source code (for OSX users)
-----------------------------------------------
0. Install [homebrew](http://brew.sh/).
1. Execute `brew install python3 qt5 pyqt5`.
2. Execute `pip3 install -r requirements.txt`.


How to launch from source code (for Windows users)
---------------------------------------------------
0. Install python3.
1. Execute `pip3 install -r requirements.txt`.
2. Install [PyQt5 for windows](https://riverbankcomputing.com/software/pyqt/download5) binary package.

Note: At 2015/12/3, PyQt5.5.1 binary package supports only python3.4.


How to use
-----------
0. Start app with `python FSECplotter2.py`.
1. Drag and Drop the FSEC logfile(s) to the left-side widget. 
Or, press "Open File" button and select logfiles.
2. Chromatograms will appear in right half widget.
3. To save figure, press "Save Fig. As..." button to select filename to save. 
PNG, JPG, PDF formats can be selected.
4. "Quick Save" button saves figure as `YYMMDD-HHMMSS.png` format in the last loaded directory.
5. If you want to delete all files, press 'file'->'Remove all files'.

+ flowrate data was automatically parsed when decimal was contained in the method filename in Shimadzu format. For other HPLC formats, please input the flowrate information manually.

+ In the FSEC-TS calculation, the temperature information will be automatically parsed when integer was contained in the filename of data file.


Test files
------------
This repository includes test files for Shimadzu HPLC in `test/fixture/shimadzu` directory.

+   `test?.txt` :
    test files for large column (GE Healthcare Superose6 increase 10/300)

+   `mini_test?.txt` :
    test files for mini column (GE Healthcare Superdex200 increase 5/150)

Or, for Hitachi HPCL, use the test files in `test/fixture/hitachi` directory

+   `*.rw?` :
    for wave length 1 or 2

Packaging
-----------
Packaged binary for Windows and MacOSX is distributed in `release` tab above.

If you want to build binary yourself, use [Pyinstaller](http://www.pyinstaller.org/) for example.

For pyinstaller, use the spec file in `win_build/FSECplotter2.spec` or `osx_build/FSECplotter2.spec`, 
as `pyinstaller --clean FSECplotter2.spec`


For Another HPLC
------------------
To extend for another HPLC,

0. Extend the `Logfile` class in `FSECplotter/core/logfile.py`, and implement `data()` and `_parse()` method.
1. Add dispatch code to `LogfileFactory.create()` method in `FSECplotter/core/logfile`.

License
--------
+ GPLv2
