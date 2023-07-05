from setuptools import setup, find_packages

setup(
    name='htr_cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'plotext'
    ],
    entry_points={
        'console_scripts': [
            'htr = htr.cli.cli:cli',
        ],
    },
)