from setuptools import setup, find_packages

setup(
    name='datastorm',
    version='0.0.0a4',
    description='Simple and easy to use ODM for Google Datastore',
    url='https://github.com/JavierLuna/datastorm',
    author='Javier Luna Molina',
    author_email='jlunadevel@gmail.com',
    install_requires=['google-cloud-datastore'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='object document mapping odm datastore google google-cloud google-datastore',
    packages=find_packages(exclude=['docs', 'examples', 'tests'])
)
