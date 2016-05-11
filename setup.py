from setuptools import setup, find_packages

setup(
    name='dlint',
    version='0.0.1',
    packages=find_packages(),
    scripts=['bin/dlint'],
    author="Jerome Pin",
    author_email="jeromepin38@gmail.com",
    description="A simple nonprofessional Dockerfile linter",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/jeromepin/dlint',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Bug Tracking",
    ]
)
