from setuptools import setup, find_packages
import os

version = '1.1.1'

tests_require = [
    'zope.configuration',
    'zope.app.wsgi',
    'zope.testing',
    'zope.publisher',
    'zeam.form.base [test]',
    ]

setup(name='zeam.form.table',
      version=version,
      description="Form as table, to edit more than one content at a time",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zeam form table',
      author='Sylvain Viollon',
      author_email='thefunny@gmail.com',
      url='http://pypi.python.org/pypi/zeam.form.table',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['zeam', 'zeam.form'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'grokcore.component',
        'grokcore.chameleon',
        'megrok.pagetemplate',
        'setuptools',
        'zeam.form.base >= 1.2.3',
        'zeam.form.composed >= 1.3',
        'zeam.utils.batch >= 1.0',
        'zope.component',
        'zope.interface',
        'zope.i18nmessageid',
        ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
