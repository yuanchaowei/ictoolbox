from setuptools import setup

setup(
    name='ictoolbox',
    version='0.0.2',
    description='IC toolbox',
    author='Chaowei Yuan',
    #author_email='',
    packages=['icunit'],
    install_requires=["Jinja2", "numpy", "pandas", "graphviz"],
)
