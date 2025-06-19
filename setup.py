import os.path as osp
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


def find_version():
    version_file = 'torchreid/__init__.py'
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def get_requirements(filename='requirements.txt'):
    here = osp.dirname(osp.realpath(__file__))
    with open(osp.join(here, filename), 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def build_extensions():
    try:
        import numpy as np
    except ImportError:
        raise RuntimeError("numpy must be installed before building torchreid. Try: pip install numpy")

    try:
        from Cython.Build import cythonize
        from distutils.extension import Extension
    except ImportError:
        raise RuntimeError("Cython must be installed before building torchreid. Try: pip install Cython")

    try:
        numpy_include = np.get_include()
    except AttributeError:
        numpy_include = np.get_numpy_include()

    ext_modules = [
        Extension(
            'torchreid.metrics.rank_cylib.rank_cy',
            ['torchreid/metrics/rank_cylib/rank_cy.pyx'],
            include_dirs=[numpy_include],
        )
    ]
    return cythonize(ext_modules)


setup(
    name='torchreid',
    version=find_version(),
    description='A library for deep learning person re-ID in PyTorch',
    author='Kaiyang Zhou',
    license='MIT',
    long_description=readme(),
    url='https://github.com/KaiyangZhou/deep-person-reid',
    packages=find_packages(),
    install_requires=get_requirements(),
    keywords=['Person Re-Identification', 'Deep Learning', 'Computer Vision'],
    ext_modules=build_extensions(),
)
