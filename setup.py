import setuptools


with open("README.rst", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="django-liquid",
    version="1.0.0",
    description="A Django template backend for Liquid.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/jg-rp/django-liquid",
    packages=setuptools.find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["django>=2.2", "python-liquid[autoescape]>=0.7.4"],
    test_suite="tests",
    python_requires=">=3.7",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    project_urls={
        "Documentation": "https://jg-rp.github.io/liquid/guides/django-liquid",
        "Issue Tracker": "https://github.com/jg-rp/django-liquid/issues",
        "Source Code": "https://github.com/jg-rp/django-liquid",
    },
)
