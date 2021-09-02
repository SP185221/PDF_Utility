import sys
from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR=os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR,'tcl','tk8.6')

include_files = [(os.path.join(PYTHON_INSTALL_DIR,'DLLs','tk86.dll'),os.path.join('lib''tk86.dll')), (os.path.join(PYTHON_INSTALL_DIR,'DLLs','tcl86t.dll'),os.path.join('lib''tcl86.dll')) ]
base = None

if sys.platform == 'win32':
    base='Win32GUI'

executables = [Executable('PDF_Projects.py', base=base, icon= r"C:\Users\sp185\Desktop\PDF PROJECTS\pdf.ico", shortcutName='NcrPDF', shortcutDir = "DesktopFolder")]

setup(name= 'NCR PDF Utility ', version = '3.3.2', author = 'NCR India', description = 'PDF Utility',  options = { 'buils_exe': {'include_files': include_files}}, executables = executables )