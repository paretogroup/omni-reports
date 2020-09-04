import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='omni_reports',
    packages=setuptools.find_packages(),
    version='0.0.6',
    description='Omni Report Definition',
    author='Pareto Group',
    author_email='noreply@paretogroup.com.br',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/paretogroup/omni-reports',
    keywords=['pareto', 'api', 'reports'],
    classifiers=[],
)
