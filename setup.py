from setuptools import setup, find_packages

setup(
    name="arxiv-accelerator-physics",
    version="1.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.8.0",
        "aiofiles>=23.1.0",
        "openai>=1.0.0",
        "anthropic>=0.25.0",
        "PyYAML>=6.0",
        "python-dateutil>=2.8.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "requests>=2.31.0",
        "urllib3>=2.0.0",
        # Web界面依赖 (v1.1.0新增)
        "Flask>=2.3.0",
        "Werkzeug>=2.3.0", 
        "Jinja2>=3.1.0",
        "MarkupSafe>=2.1.0",
    ],
    python_requires=">=3.8",
)
