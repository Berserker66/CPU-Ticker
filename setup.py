import sys
from cx_Freeze import setup, Executable
from pathlib import Path
import sysconfig
import os

is_64bits = sys.maxsize > 2**32

folder = "exe.{platform}-{version}".format(platform = sysconfig.get_platform(),
                                           version = sysconfig.get_python_version())
buildfolder = Path("build", folder)


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages" : "Language"}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
targetname = None
targetname2 = None
if sys.platform == "win32":
    base = "Win32GUI"
    targetname = "Ticker.exe"
    targetname2 = "Console.exe"

setup(  name = "CPU Ticker",
        version = "2.0",
        #description = "",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui.py", base=base, targetName=targetname),
                       Executable("console.py", targetName=targetname2)])

if sys.platform == "win32" and os.path.isfile("upx.exe"):
    strbuild = str(buildfolder)
    targets = os.listdir(strbuild)
    targets = filter(lambda x:x.endswith((".pyd", ".exe")), targets)
    targets = " ".join((os.path.join(strbuild, target) for target in targets))
    command = "upx.exe "+targets
    print(command)
    os.system(command)