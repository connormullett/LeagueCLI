
from setuptools import setup

setup(
    name='leaguecli',
    author='Connor Mullett',
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'league=leaguecli.__main__:main'
        ]
    }
)
