from setuptools import setup

setup(
    name='devkit',
    version='0.1',
    py_modules=['devkit'],
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'devkit = devkit:devkit'
        ]
    }
)
