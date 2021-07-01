from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='pbpy',
    version='1.0.2',
    description="Wrapper per l'api di primebots.it",
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Giuseppe Pollio',
    author_email='polliog@protonmail.com',
    keywords=['primebots', 'pbpy'],
    url='https://pypi.org/project/pbpy',
    download_url='https://github.com/Polliog/primebots-py-wrapper'
)

install_requires = [
    'requests',
    'discord.py',
    'asyncio',
    'python-socketio[asyncio_client]'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
