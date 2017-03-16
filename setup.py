import os
import sys
from distutils.core import setup, Command
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import versioneer

class CleanInplace(Command):
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        files = ['accumuloadapter/core/AccumuloAdapter.cpp']
        for file in files:
            try:
                os.remove(file)
            except OSError:
                pass


def setup_accumulo(include_dirs, lib_dirs):
    src = ['accumuloadapter/core/AccumuloAdapter.pyx',
           'accumuloadapter/core/accumulo_adapter.cpp',
           'accumuloadapter/core/AccumuloProxy.cpp',
           'accumuloadapter/core/proxy_types.cpp',
           'accumuloadapter/core/proxy_constants.cpp']

    extra_compile_args = []
    if sys.platform == 'win32':
        vc_version = os.getenv("VS_MAJOR")
        libs = ['thrift',
                'boost_thread-vc%s0-mt-1_61'%vc_version,
                'boost_system-vc%s0-mt-1_61'%vc_version,
                'boost_chrono-vc%s0-mt-1_61'%vc_version]
        extra_compile_args.append('/D BOOST_ALL_DYN_LINK')
    else:
        libs = ['thrift']
        #extra_compile_args = ['-std=c++11']

    return Extension('accumuloadapter.core.AccumuloAdapter',
                     src,
                     language='c++',
                     include_dirs=include_dirs,
                     library_dirs=lib_dirs,
                     libraries=libs,
                     extra_compile_args=extra_compile_args)


def run_setup():

    include_dirs = [os.path.join('accumuloadapter', 'lib'),
                    numpy.get_include()]
    if sys.platform == 'win32':
        include_dirs.append(os.path.join(sys.prefix, 'Library', 'include'))
    else:
        include_dirs.append(os.path.join(sys.prefix, 'include'))

    lib_dirs = []
    if sys.platform == 'win32':
        lib_dirs.append(os.path.join(sys.prefix, 'Library', 'lib'))
    else:
        lib_dirs.append(os.path.join(sys.prefix, 'lib'))

    ext_modules = []
    packages = ['accumuloadapter', 'accumuloadapter.lib', 'accumuloadapter.tests']
    ext_modules.append(setup_accumulo(include_dirs, lib_dirs))
    packages.append('accumuloadapter.core')

    versioneer.versionfile_source = 'accumuloadapter/_version.py'
    versioneer.versionfile_build = 'accumuloadapter/_version.py'
    versioneer.tag_prefix = ''
    versioneer.parentdir_prefix = 'accumuloadapter-'

    cmdclass = versioneer.get_cmdclass()
    cmdclass['build_ext'] = build_ext
    cmdclass['cleanall'] = CleanInplace

    setup(name='accumuloadapter',
          version = versioneer.get_version(),
          description='optimized IO for NumPy/Blaze',
          author='Continuum Analytics',
          author_email='support@continuum.io',
          ext_modules=ext_modules,
          packages=packages,
          cmdclass=cmdclass)


if __name__ == '__main__':
    run_setup()
