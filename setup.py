from setuptools import setup

setup(
    name="booklog",
    version="1.0",
    packages=["booklog", "booklog.cli"],
    entry_points={"console_scripts": ["booklog = booklog.cli.main:prompt"]},
)
