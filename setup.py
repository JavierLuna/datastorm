from setuptools import setup, find_packages
import datastorm

setup(
    name='datastorm',
    version=datastorm.__version__,
    description='Simple and easy to use ODM for Google Datastore. Documentation: https://datastorm-docs.rtfd.io',
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
