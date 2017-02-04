import pathlib
from setuptools import setup
from aiounfurl import VERSION


readme_file_path = pathlib.Path(__file__).parent / 'README.md'
setup(
    name="aiounfurl",
    version=".".join(map(str, VERSION)),
    author="Igor Tokarev",
    author_email="TigorC@gmail.com",
    description='Making site preview',
    long_description=readme_file_path.read_text(),
    license="BSD License",
    keywords="async embed preview",
    url="https://github.com/tigorc/aiounfurl",
    include_package_data=True,
    install_requires=[
        'setuptools',
        'beautifulsoup4',
        'html5lib',
        'aiohttp'],
    packages=['aiounfurl'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP"
    ],
)
