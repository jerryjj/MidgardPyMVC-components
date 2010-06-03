try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='midgardmvc-fi.infigo.account',
    version='0.1',
    description='User account management component for MidgardPyMVC',
    author='Jerry Jalava',
    author_email='jerry.jalava@infigo.fi',
    url='',
    namespace_packages = ['midgardmvc', 'midgardmvc.components', 'midgardmvc.controllers'],
    # install_requires=[
    #     "midgardmvc>=0.1",
    # ],
    test_suite='nose.collector',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'midgardmvc.components.fi_infigo_account': ['i18n/*/LC_MESSAGES/*.mo', 'public/midcom-static/fi.infigo.account/*']},
    message_extractors={'midgardmvc.components.fi_infigo_account': [
           ('**.py', 'python', None),
           ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
           ('public/**', 'ignore', None)],
           'midgardmvc.controllers.fi_infigo_account': [
                ('**.py', 'python', None)]},
    zip_safe=False,
    entry_points="""
    [midgardmvc.component]
    fi.infigo.account = midgardmvc.components.fi_infigo_account:make_component
    """,
)
