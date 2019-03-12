
from setuptools import setup

setup(
    name='leaguecli',
    author='Connor Mullett',
    version='0.1.0',
    package_data={'': ['leaguecli/settings.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'league=leaguecli.main:main'
        ]
    }
)
