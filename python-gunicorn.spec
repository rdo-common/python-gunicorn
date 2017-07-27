
%global upstream_name gunicorn

Name:           python-%{upstream_name}
Version:        19.7.1
Release:        2%{?dist}
Summary:        Python WSGI application server
License:        MIT
URL:            http://gunicorn.org/
Source0:        https://files.pythonhosted.org/packages/source/g/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
# We already have aiohttp 2.x in F27+ so we need this fix now, to get the tests passing
# https://github.com/benoitc/gunicorn/pull/1418
Patch1:         deprecate-gaiohttp-worker.patch
# distro-specific, not upstreamable
Patch101:       0001-use-dev-log-for-syslog.patch
# upstream version requirements are unnecessarily strict
Patch102:       0002-relax-version-requirements.patch
BuildArch:      noarch

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.

%package -n python2-%{upstream_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{upstream_name}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python2-mock
BuildRequires:  python2-pytest-cov
BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinx_rtd_theme
Requires:       python2-setuptools

%description -n python2-%{upstream_name}
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.

%package -n python3-%{upstream_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{upstream_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
Requires:       python3-setuptools

%description -n python3-%{upstream_name}
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.

%package doc
Summary:        Documentation for the %{name} package

%description doc
Documentation for the %{name} package.

%prep
%setup -q -n %{upstream_name}-%{version}
%patch1 -p1
%patch101 -p1
%patch102 -p1

%build
%py2_build
%py3_build
%{__python2} setup.py build_sphinx

%install
%py3_install
# rename executables in /usr/bin so they don't collide
for executable in %{upstream_name} %{upstream_name}_paster ; do
    mv %{buildroot}%{_bindir}/$executable %{buildroot}%{_bindir}/python3-$executable
done
%py2_install
# need to remove gaiohttp worker from the Python 2 version, it is supported on 
# Python 3 only and it fails byte compilation on 2.x due to using "yield from"
rm %{buildroot}%{python2_sitelib}/%{upstream_name}/workers/_gaiohttp.py*

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{upstream_name}
%license LICENSE
%doc NOTICE README.rst THANKS
%{python2_sitelib}/%{upstream_name}*
%{_bindir}/%{upstream_name}
%{_bindir}/%{upstream_name}_paster

%files -n python3-%{upstream_name}
%license LICENSE
%doc NOTICE README.rst THANKS
%{python3_sitelib}/%{upstream_name}*
%{_bindir}/python3-%{upstream_name}
%{_bindir}/python3-%{upstream_name}_paster

%files doc
%license LICENSE
%doc build/sphinx/html/*

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 19.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Dan Callaghan <dcallagh@redhat.com> - 19.7.1-1
- upstream release 19.7.1: http://docs.gunicorn.org/en/19.7.1/news.html

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 19.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 19.6.0-3
- Rebuild for Python 3.6

* Mon Aug 15 2016 Dan Callaghan <dcallagh@redhat.com> - 19.6.0-2
- updated to latest Python guidelines

* Mon Aug 15 2016 Dan Callaghan <dcallagh@redhat.com> - 19.6.0-1
- upstream release 19.6.0: http://docs.gunicorn.org/en/19.6.0/news.html

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.4.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 19.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Dan Callaghan <dcallagh@redhat.com> - 19.4.1-1
- upstream release 19.4.1: http://docs.gunicorn.org/en/19.4.1/news.html

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 05 2015 Dan Callaghan <dcallagh@redhat.com> - 19.3.0-3
- handle expected HaltServer exception in manage_workers (RHBZ#1200041)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 09 2015 Dan Callaghan <dcallagh@redhat.com> - 19.3.0-1
- upstream release 19.3.0: http://docs.gunicorn.org/en/19.3.0/news.html

* Tue Aug 19 2014 Dan Callaghan <dcallagh@redhat.com> - 19.1.1-2
- fixed build requirements, added -doc subpackage with HTML docs

* Tue Aug 19 2014 Dan Callaghan <dcallagh@redhat.com> - 19.1.1-1
- upstream release 19.1.1: http://docs.gunicorn.org/en/19.1.1/news.html

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
