try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='midgardmvc-fi.infigo.chat',
    version='0.1',
    description='Example MidgardPyMVC Component',
    author='Jerry Jalava',
    author_email='jerry.jalava@iki.fi',
    url='',
    namespace_packages = ['midgardmvc', 'midgardmvc.components', 'midgardmvc.controllers'],
    install_requires=[
        #"midgardmvc>=0.1",
        "cogen",
    ],
    test_suite='nose.collector',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'midgardmvc.components.fi_infigo_chat': ['i18n/*/LC_MESSAGES/*.mo', 'public/midcom-static/fi.infigo.chat/*']},
    message_extractors={'midgardmvc.components.fi_infigo_chat': [
           ('**.py', 'python', None),
           ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
           ('public/**', 'ignore', None)],
           'midgardmvc.controllers.fi_infigo_chat': [
                ('**.py', 'python', None)]},
    zip_safe=False,
    entry_points="""
    [midgardmvc.component]
    chat = midgardmvc.components.fi_infigo_chat:make_component
    """,
)
