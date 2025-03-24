import pyqt5ac

ioPaths = [
    ["./*.ui", "./%%FILENAME%%.py"],
    ["./*.qrc", "./%%FILENAME%%_rc.py"],
]

pyqt5ac.main(
    rccOptions="",
    uicOptions="--from-imports",
    force=False,
    config="",
    ioPaths=ioPaths,
    variables=None,
    initPackage=True,
)
