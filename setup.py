from setuptools import setup, find_packages

setup(
    name="duplicati-prometheus-exporter",
    version="0.1.0",
    author="Lucas Aleixo",
    author_email="aleixo2lucas@gmail.com",
    description="A simple prometheus exporter for Duplicati backup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AleixoLucas42/duplicati-promethes-exporter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["Flask==3.0.3", "Flask-Cors==4.0.0", "prometheus_client==0.20.0","pytz==2024.1"],
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/AleixoLucas42/duplicati-promethes-exporter/issues",
        "Source": "https://github.com/AleixoLucas42/duplicati-promethes-exporter",
    },
)
