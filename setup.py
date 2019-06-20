from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="kronos",
    version="0.0.1",
    description="d-hacks cli",
    author="d-hacks",
    packages=find_packages(),
    package_data={
        'kronos': ['src/docker/*', 'src/kronos-config.yml', 'src/.gitignore']
    },
    entry_points={
        "console_scripts": [
            "kronos=kronos.core:main",
        ]
    },
    install_requires=[
        'click',
        'oyaml',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
