from setuptools import setup, find_packages

with open('../README.md') as readme_file:
    README = readme_file.read()
"""
with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()
"""
setup_args = dict(
    name='pyNAVIS',
    version='1.0.1',
    description='Useful tools to analyze and process spiking information from neuromorphic auditory sensors.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL',
    packages=find_packages(),
    author='Juan P. Dominguez-Morales',
    author_email='jpdominguez@atc.us.es',
    keywords=['pyNAVIS', 'NAVIS', 'neuromorphic engineering', "neuromorphic audio processing", "neuromorphic sensors"],
    url='https://github.com/jpdominguez/pyNAVIS',
    download_url='https://pypi.org/project/pyNAVIS/'
)

install_requires = [
	'matplotlib',
	'numpy',
	'scipy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)