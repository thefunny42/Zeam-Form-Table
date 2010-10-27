from setuptools import setup, find_packages
import os

version = '1.0b1'

tests_require = [
    'zope.securitypolicy',
    'zope.app.authentication',
    'zope.app.testing',
    'zope.app.zcmlfiles',
    'zope.testing',
    'zope.testbrowser',
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
        'megrok.pagetemplate',
        'setuptools',
        'zeam.form.base',
        'zeam.form.composed',
        'zope.component',
        'zope.interface',
        ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
