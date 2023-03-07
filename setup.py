from distutils.core import setup

setup(
    name="omega2auto",
    version="0.1",
    description="Python module for converting the OMEGA format into A.U.T.O. ABoxes",
    author ="Lukas Westhofen",
    author_email="lukas.westhofen@dlr.de",
    install_requires=[
        "pyauto",
        "omega_format",
        "shapely"
    ]
)
