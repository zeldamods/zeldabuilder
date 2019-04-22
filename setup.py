import fastentrypoints
import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zeldabuilder",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="leoetlino",
    author_email="leo@leolam.fr",
    description="Tools to build and unbuild a Zelda ROM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeldamods/builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["rstb~=1.0", "aamp~=1.3", "byml~=2.2", "sarc~=2.0", "wszst-yaz0~=1.2", "xxhash~=1.3"],
    entry_points = {
        "console_scripts": [
            "zeldabuilder = zeldabuilder.main:main",
        ],
    },
)
