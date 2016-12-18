from setuptools import setup


setup(
    name="aiounfurl",
    version="0.1",
    author="Igor Tokarev",
    author_email="TigorC@gmail.com",
    description="Extract information from web page",
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
