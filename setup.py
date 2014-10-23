# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a2.dev0'
description = 'Plone integration with CiviCRM.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.civicrm',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='civicrm rest api plone',
    author='Simples Consultoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.civicrm',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gevent',
        'plone.api',
        'plone.app.registry',
        'plone.app.upgrade',
        'plone.app.users',
        'plone.directives.form',
        'plone.memoize',
        'Products.CMFPlone >=4.2',
        'Products.CMFQuickInstallerTool',
        'Products.GenericSetup',
        'profilehooks',
        'requests',
        'setuptools',
        'zExceptions',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'httmock',
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'robotsuite',
            'zope.component',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
