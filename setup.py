import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywgen",
    author="Denis Laxalde",
    author_email="denis@laxalde.org",
    description="generate pronounceable passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~dlax/pywgen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["pywgen=pywgen:main"]},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
