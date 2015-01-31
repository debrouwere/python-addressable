from setuptools import setup, find_packages

setup(name='addressable',
      description='Use lists like you would dictionaries.',
      long_description=open('README.rst').read(),
      author='Stijn Debrouwere',
      author_email='stijn@debrouwere.org',
      url='https://github.com/debrouwere/python-addressable/',
      download_url='http://www.github.com/debrouwere/python-addressable/tarball/master',
      version='1.3.0',
      license='ISC',
      packages=find_packages(),
      install_requires=[
            'pylev>=1',      
            ], 
      keywords='utility',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities',
                   ],
      )