
%global upstream_name gunicorn

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        19.0.0
Release:        1%{?dist}
Summary:        Python WSGI application server

Group:          System Environment/Daemons
License:        MIT
URL:            http://gunicorn.org/
Source0:        http://pypi.python.org/packages/source/g/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
# distro-specific, not upstreamable
Patch100:       %{name}-dev-log.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
%endif

Requires:       python-setuptools

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python WSGI application server
Requires:       python3-setuptools

%description -n python3-%{upstream_name}
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
%patch100 -p1

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

# need to remove gaiohttp worker from the Python 2 version, it is supported on 
# Python 3 only and t fails byte compilation on 2.x due to using "yield from"
rm gunicorn/workers/gaiohttp.py*

%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
# rename executables in /usr/bin so they don't collide
for executable in %{upstream_name} %{upstream_name}_django %{upstream_name}_paster ; do
    mv %{buildroot}%{_bindir}/$executable %{buildroot}%{_bindir}/python3-$executable
done
popd
%endif

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%files
%doc LICENSE NOTICE README.rst THANKS
%{python_sitelib}/%{upstream_name}*
%{_bindir}/%{upstream_name}
%{_bindir}/%{upstream_name}_django
%{_bindir}/%{upstream_name}_paster

%if %{with python3}
%files -n python3-%{upstream_name}
%doc LICENSE NOTICE README.rst THANKS
%{python3_sitelib}/%{upstream_name}*
%{_bindir}/python3-%{upstream_name}
%{_bindir}/python3-%{upstream_name}_django
%{_bindir}/python3-%{upstream_name}_paster
%endif

%changelog
* Mon Jun 23 2014 Dan Callaghan <dcallagh@redhat.com> - 19.0.0-1
- upstream release 19.0: http://docs.gunicorn.org/en/19.0/news.html

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Sep 06 2013 Dan Callaghan <dcallagh@redhat.com> - 18.0-1
- upstream release 18.0: http://docs.gunicorn.org/en/latest/news.html

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Dan Callaghan <dcallagh@redhat.com> - 17.5-1
- upstream release 17.5: 
  http://docs.gunicorn.org/en/R17.5/2013-news.html#r17-5-2013-07-03 
  (version numbering scheme has changed to drop the initial 0)

* Tue Apr 30 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.4-1
- upstream release 0.17.4: http://docs.gunicorn.org/en/0.17.4/news.html

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.2-1
- upstream bug fix release 0.17.2

* Wed Jan 02 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.0-2
- patch to use /dev/log for syslog by default

* Wed Jan 02 2013 Dan Callaghan <dcallagh@redhat.com> - 0.17.0-1
- new upstream release 0.17.0

* Mon Nov 26 2012 Dan Callaghan <dcallagh@redhat.com> - 0.16.1-2
- fix test suite error with py.test on Python 3.3

* Mon Nov 26 2012 Dan Callaghan <dcallagh@redhat.com> - 0.16.1-1
- new upstream release 0.16.1 (with Python 3 support)

* Mon Oct 22 2012 Dan Callaghan <dcallagh@redhat.com> - 0.15.0-1
- new upstream release 0.15.0

* Mon Aug 20 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.6-2
- fix for LimitRequestLine test failure (upstream issue #390)

* Wed Aug 01 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.6-1
- upstream bugfix release 0.14.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.5-1
- upstream bugfix release 0.14.5

* Thu Jun 07 2012 Dan Callaghan <dcallagh@redhat.com> - 0.14.3-1
- updated to upstream release 0.14.3

* Wed Feb 08 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-3
- renamed package to python-gunicorn, and other minor fixes

* Tue Jan 31 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-2
- patch for failing test (gunicorn issue #294)

* Mon Jan 30 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-1
- initial version
