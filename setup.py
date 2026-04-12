from setuptools import setup, find_packages

setup(
    name='django-auto-api-gen',
    version='1.3.0',
    description='A utility to auto-generate Django REST Framework serializers and API ViewSets for models in specified apps',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Amer Al-Jabri',
    author_email='amerprogrammer85@gmail.com',
    url='https://github.com/Amer-Tawfiq/django-auto-api-gen',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'djangorestframework',
        'django-filter',
        'drf-spectacular',
        'djangorestframework-simplejwt',
        'black',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
