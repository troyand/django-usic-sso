from distutils.core import setup

setup(
    name='django-usic-sso',
    version='0.2.5',
    author='Mykhailo Troianovskyi',
    author_email='troyanovsky@gmail.com',
    packages=['django_usic_sso',],
    url='https://github.com/troyand/django-usic-sso',
    license='GPLv2',
    description='Authentication backend for Django that utilizes USIC Redis SSO cookie.',
    install_requires=[
        'Django >= 1.4',
        'redis >= 2.4.10',
        'phpserialize >= 1.3',
    ],
)

