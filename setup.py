from setuptools import setup

def description():
    return open('README.md').read()

setup(
    name='totpy',
    version='0.1.3',
    author='Jorge García',
    author_email='jorgegarciadev@icloud.com',
    description='Totpy - CLI TOTP generator and managemet tool',
    long_description = description(),
    long_description_content_type='text/markdown',
    url='https://github.com/jorgegarciadev/totpy',
    license='MIT',
    py_modules=['totpy'],
    install_requires=[
        'Click==7.0',
        'Pillow==7.0.0',
        'Pypng==0.0.20',
        'PyQRCode==1.2.1',
        'pyzbar==0.1.8'
    ],
    entry_points={
        'console_scripts': {
            'totpy = totpy:main'
        }
    },
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers', 
    'Intended Audience :: End Users/Desktop',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    ],
    keywords='2fa authenticator totp hotp otp'
)