from setuptools import setup, find_packages

setup(
    name="correlactions",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "requests",
        "pandas",
        "numpy",
        "scipy",
        "plotly",
        "python-dotenv",
    ],
) 