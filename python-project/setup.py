from setuptools import setup

setup(
    name="skunky",
    version="0.0.1",
    packages=["skunky"],
    entry_points={
        'console_scripts': [
            # When I run 'skunky' from the command line, it will run the 'main' function in skunky/__init__.py
            # Homebrew will automatically install a bin to do this.
            'skunky=skunky:main', 
        ],
    },
)