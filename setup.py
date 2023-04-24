from setuptools import setup
import re
import os


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('django_database_cipher')

setup(
    name='django-database-cipher',
    version=version,
    description="Database cipher support for Django",
    long_description="This module allows your Django project to work with SQLCipher.",
    author="Raison Chan",
    author_email="raisonschan@gmail.com",
    url="https://github.com/raisons/django-database-cipher",
    license="MIT",
    platforms=["any"],
    install_requires=[
        # 'django>=3.1',
        # 'pysqlcipher3'
    ],
    packages=get_packages('django_database_cipher'),
    package_data=get_package_data('django_database_cipher'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Security :: Cryptography",
    ],
    include_package_data=True,
)
