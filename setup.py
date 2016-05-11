"""
This package installs a pth file that enables the coveragepy process_startup
feature in this python prefix/virtualenv in subsequent runs.

See: http://nedbatchelder.com/code/coverage/subprocess.html


Demo::

    $ virtualenv tmpenv
    $ . tmpenv/bin/activate
    $ pip install coverage-enable-subprocess
    $ touch .coveragerc
    $ export COVERAGE_PROCESS_START=$PWD/.coveragerc
    $ echo 'print("oh, hi!")' > ohhi.py
    $ python ohhi.py
    oh, hi!

    $ coverage report
    Name                              Stmts   Miss  Cover
    -----------------------------------------------------
    /etc/python2.6/sitecustomize.py       5      1    80%
    ohhi.py                               1      0   100%
    tmpenv/lib/python2.6/site.py        433    392     9%
    -----------------------------------------------------
    TOTAL                               439    393    10%


For projects that need to cd during their test runs, and run many processes in parallel,
I ensure a ``$TOP`` variable is exported, and I use this .coveragerc::

    [run]
    parallel = True
    branch = True
    data_file = $TOP/.coverage

    [report]
    exclude_lines =
        # Have to re-enable the standard pragma
        \\#.*pragma:\\s*no.?cover

        # we can't get coverage for functions that don't return:
        \\#.*never returns
        \\#.*doesn't return

        # Don't complain if tests don't hit defensive assertion code:
        ^\\s*raise Impossible\\b
        ^\\s*raise AssertionError\\b
        ^\\s*raise NotImplementedError\\b
        ^\\s*return NotImplemented\\b

        # Don't complain if tests don't hit re-raise of unexpected errors:
        ^\\s*raise$

        # if main is covered, we're good:
        ^\\s*exit\\(main\\(\\)\\)$
    show_missing = True

    [html]
    directory = $TOP/coverage-html

    # vim:ft=dosini
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from distutils import log

from setuptools import setup
from setuptools.command.install import install as orig_install

PTH = '''\
try:
    import coverage
# coverage throws OSError when $PWD does not exist
except (ImportError, OSError):
    pass
else:
    coverage.process_startup()
'''

DOC = __doc__


class Install(orig_install):
    """
    default semantics for install.extra_path cause all installed modules to go
    into a directory whose name is equal to the contents of the .pth file.

    All that was necessary was to remove that one behavior to get what you'd
    generally want.
    """
    # pylint:disable=no-member,attribute-defined-outside-init,access-member-before-definition

    def initialize_options(self):
        orig_install.initialize_options(self)
        name = self.distribution.metadata.name

        contents = 'import sys; exec(%r)\n' % PTH
        self.extra_path = (name, contents)

    def finalize_options(self):
        orig_install.finalize_options(self)

        from os.path import relpath, join
        install_suffix = relpath(self.install_lib, self.install_libbase)
        if install_suffix == '.':
            log.info('skipping install of .pth during easy-install')
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            log.info(
                "will install .pth to '%s.pth'",
                join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                'unexpected install_suffix',
                self.install_lib, self.install_libbase, install_suffix,
            )


def main():
    """the entry point"""
    setup(
        name=str('coverage_enable_subprocess'),
        version='1.0',
        url="https://github.com/bukzor/python-coverage-enable-subprocess",
        license="MIT",
        author="Buck Evan",
        author_email="buck.2019@gmail.com",
        description="enable python coverage for subprocesses",
        long_description=DOC,
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'License :: OSI Approved :: MIT License',
        ],
        install_requires=[
            'coverage',
        ],
        cmdclass={
            'install': Install,
        },
        options={
            'bdist_wheel': {
                'universal': 1,
            },
        },
    )


if __name__ == '__main__':
    exit(main())
