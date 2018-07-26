import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='score.sass',
    version='0.0.3',
    description='Sass integration for The SCORE Framework',
    long_description=README,
    author='strg.at',
    author_email='score@strg.at',
    url='http://score-framework.org',
    keywords='score framework web css scss sass',
    packages=['score', 'score.sass'],
    namespace_packages=['score'],
    zip_safe=False,
    license='LGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General '
            'Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'score.tpl >= 0.3',
        'libsass >= 0.7',
        'csscompressor >= 0.9',
    ],
)
