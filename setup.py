try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='predicrystal',
    version='0.1.0',
    description='Python module to read/write SerialEM .nav files.',
    python_requires='>=3.6*',
    author='Arent Kievits',
    packages=[],
    package_dir={
        '': '.'},
    package_data={},
    entry_points={
        'console_scripts': [
            'generate_test_data = predicrystal.generate_test_data:main',
            'run_ilastik = predicrystal.run_ilastik_cmndline:main',
            'results_to_nav = predicrystal.ilastik_results_to_nav:main',
            'predicrystal.generate_test_data = predicrystal.generate_test_data:main',
            'predicrystal.run_ilastik = predicrystal.run_ilastik_cmndline:main',
            'predicrystal.results_to_nav = predicrystal.ilastik_results_to_nav:main',
        ],
    },
)
