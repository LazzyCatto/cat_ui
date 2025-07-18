from setuptools import setup, find_packages

setup(
    name="cat_ui",
    version="1.0.5",
    description="Simple python ui lib for cli programs",
    author="Akio Smiowly",
    author_email="lazzycatto@yandex.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "regex>=2024.11.6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
