#! /usr/bin/env python

"""
`doit` comes from the idea of bringing the power of build-tools to execute any
 kind of task. It will keep track of dependencies between "tasks" and execute
 them only when necessary. It was designed to be easy to use and "get out of
 your way".

`doit` can be used as:

 * a build tool (generic and flexible)
 * home of your management scripts (it helps you organize and combine shell
   scripts and python scripts)
 * a functional tests runner (combine together different tools)
 * a configuration management system
 * manage computational pipelines

Features:

 * Easy to use, "no-API"
 * Use python to dynamically create tasks on-the-fly
 * Flexible, adapts to many workflows for creation of tasks/rules/recipes
 * Support for multi-process parallel execution
 * Built-in integration of inotify (automatically re-execution)

In `doit`, unlike most (all?) build-tools, a task doesn't need to define a
 target file to use the execute only if not up-to-date feature. This make
 `doit` specially suitable for running a sub-set of your test suites.

`doit` like most build tools is used to execute tasks defined in a
 configuration file. Configuration files are python modules. The tasks can be
 python functions or an external shell script/command. `doit` automatically
 keeps track of declared dependencies executing only tasks that needs to be
 updated

If you are still wondering why someone would want to use this tool,
 check this blog
 `post <http://schettino72.wordpress.com/2008/04/14/doit-a-build-tool-tale/>`_.
"""

from distutils.core import setup, Command

import sys
if sys.version_info >= (3,0):
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

########### platform specific stuff #############
import platform
platform_system = platform.system()

install_requires = []
# auto command dependencies to watch file-system
if platform_system == "Darwin":
    install_requires.append('macfsevents')
elif platform_system == "Linux":
    install_requires.append('pyinotify')

scripts = ['bin/doit']
# platform specific scripts
if platform_system == "Windows":
    scripts.append('bin/doit.bat')

##################################################


if sys.version_info < (2, 6):
    install_requires.append('multiprocessing')
    install_requires.append('simplejson')


# http://pytest.org/goodpractises.html
class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


extra = {}
if sys.version_info >= (3,0):
    extra.update(use_2to3=True)


setup(name = 'doit',
      description = 'doit - Automation Tool',
      version = '0.14.dev',
      license = 'MIT',
      author = 'Eduardo Naufel Schettino',
      author_email = 'schettino72@gmail.com',
      url = 'http://python-doit.sourceforge.net/',
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'Environment :: Console',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Operating System :: POSIX',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.2',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: System Administrators',
                     'Topic :: Software Development :: Build Tools',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Quality Assurance',
                     'Topic :: Scientific/Engineering',
                     ],

      packages = ['doit'],
      scripts = scripts,
      cmdclass = {'test': PyTest},
      install_requires = install_requires,
      long_description = __doc__,
      **extra
      )

