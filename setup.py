from setuptools import setup, find_packages


setup(
    name='solo-filing',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'solo-filing-store = solo.filing.store:main',
            'solo-filing-analyse = solo.filing.analyse:main',
        ],
    },
)
