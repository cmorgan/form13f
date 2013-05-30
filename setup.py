from setuptools import setup, find_packages


setup(
    name='solo-filing',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'numpy',
        'nose',  # only required for running tests
    ],
    entry_points={
        'console_scripts': [
            # gives verbos answer to questions
            'solo-filing-answer= solo.filing.analyse:verbose_answer_all',
        ],
    },
)
