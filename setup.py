from setuptools import setup

from versioneer import get_cmdclass, get_version

api_requires = open("./fideslog/api/requirements.txt").read().strip().split("\n")
sdk_requires = open("./fideslog/sdk/python/requirements.txt").read().strip().split("\n")
dev_requires = open("./dev-requirements.txt").read().strip().split("\n")

setup(
    name="fideslog",
    version=get_version(),
    cmdclass=get_cmdclass(),
    description="The fideslog analytics collection mechanism",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ethyca/fideslog",
    python_requires=">=3.8, <4",
    package_dir={
        "fideslog.api": "fideslog/api",
        "fideslog.sdk.python": "fideslog/sdk/python",
    },
    packages=[
        "fideslog.api",
        "fideslog.sdk.python",
    ],
    author="Ethyca, Inc.",
    author_email="fidesteam@ethyca.com",
    license="Apache License 2.0",
    install_requires=api_requires + sdk_requires,
    dev_requires=dev_requires,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
