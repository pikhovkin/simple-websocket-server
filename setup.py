from setuptools import setup, find_packages


setup(
    name='simple-websocket-server',
    version='0.3.0',
    author='Sergei Pikhovkin',
    author_email='s@pikhovkin.ru',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description=('A simple WebSocket server'),
    long_description=open('README.md').read(),
    url='https://github.com/pikhovkin/simple-websocket-server',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
