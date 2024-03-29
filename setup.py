import os

NUMPY_VERSIONS = ['1.4.1', '1.5.0', '1.5.1', '1.6.0', '1.6.1', '1.6.2']
PYTHON_VERSIONS = ['2.6', '2.7', '3.1', '3.2']
SCIPY_VERSIONS = [None, '0.11.0']

versions = {}
for numpy_version in NUMPY_VERSIONS:
    versions['nv'] = numpy_version
    for scipy_version in SCIPY_VERSIONS:
        versions['sv'] = scipy_version
        for python_version in PYTHON_VERSIONS:
            if python_version in ['3.1', '3.2', '3.3']:
                if numpy_version == '1.4.1':
                    continue
            versions['pv'] = python_version
            versions['full'] = 'python{pv}-numpy{nv}'.format(**versions)

            if scipy_version is not None:
                versions['full'] += '-scipy{sv}'.format(**versions)

            os.system('$HOME/usr/python/bin/virtualenv-{pv} --python=$HOME/usr/python/bin/python{pv} --no-site-packages python{pv}-numpy{nv}'.format(**versions))

            # If using Python 3.3, need to update pip to the git version
            if python_version == '3.3':
                os.system('cd pip.git ; rm -r build ; ../{full}/bin/python{pv} setup.py install ; cd ..'.format(**versions))

            os.system('{full}/bin/pip-{pv} install cython'.format(**versions))

            os.system('tar xvf tarfiles/numpy-{nv}.tar'.format(**versions))
            os.chdir('numpy-{nv}'.format(**versions))
            os.system('../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**versions))
            os.system('../{full}/bin/python{pv} setup.py install'.format(**versions))
            os.chdir('../')
            os.system('rm -r numpy-{nv}'.format(**versions))

            if scipy_version is not None:

                os.system('tar xvf tarfiles/scipy-{nv}.tar'.format(**versions))
                os.chdir('scipy-{nv}'.format(**versions))
                os.system('../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**versions))
                os.system('../{full}/bin/python{pv} setup.py install'.format(**versions))
                os.chdir('../')
                os.system('rm -r scipy-{nv}'.format(**versions))
