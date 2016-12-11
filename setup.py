from setuptools import setup


setup(
    name="aiounfurl",
    version="0.1",
    author="Igor Tokarev",
    author_email="TigorC@gmail.com",
    description="Extract information from web page",
    license="BSD",
    keywords="example documentation tutorial",
    url="http://packages.python.org/an_example_pypi_project",
    include_package_data=True,
    install_requires=[
        'setuptools',
        'beautifulsoup4',
        'html5lib',
        'aiohttp'],
    packages=['aiounfurl'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
