#-*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="django-pushall",
    version='1.0.1b1',
    packages=find_packages(),
    author="Forkhammer",
    author_email="forkhammer@gmail.com",
    maintainer="Forkhammer",
    maintainer_email="forkhammer@gmail.com",
    url="https://github.com/forkhammer/django-pushall",
    license='MIT License: https://github.com/forkhammer/django-pushall/blob/master/LICENSE',
    description="Django app for Pushall notice system",
    long_description="*django-pushall* - is an application to support Push-notification system for PushAll framework Django.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=["Django>=1.8", 'requests'],
)