from setuptools import setup, find_packages

with open("CHANGELOG.txt", "r", encoding="utf-8") as f:
    cl = f.read()
    VERSION = cl.split("\"")[1]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 3.11'
]

setup(
    name='ontologytoapi',
    version=VERSION,
    description='Multi purpose API Generator based on an Ontology Framework.',
    long_description=
    f"{open('README.md').read()}\n\n" +
    f"{open('CHANGELOG.txt').read()}\n\n",
    long_description_content_type="text/markdown",
    url='https://github.com/JCGCosta/OntologyToAPI',
    author='Júlio César Guimarães Costa',
    author_email='juliocesargcosta123@gmail.com',
    license='MIT License',
    classifiers=classifiers,
    keywords=['Ontology', 'API'],
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy",
        "pydantic",
        "requests",
        "pymongo",
        "rdflib",
        "fastapi",
        "uvicorn",
        "python-multipart",
        "asyncio",
        "unqlite",
        "asyncpg",
        "aiomysql",
        "aiosqlite",
        "motor",
        "aiofiles"
    ]
)