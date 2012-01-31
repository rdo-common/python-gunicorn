Name:           gunicorn
Version:        0.13.4
Release:        2%{?dist}
Summary:        Python WSGI application server

Group:          Applications/Internet
License:        MIT
URL:            http://gunicorn.org/
Source0:        http://pypi.python.org/packages/source/g/gunicorn/gunicorn-%{version}.tar.gz
# https://github.com/benoitc/gunicorn/issues/294
Patch0:         %{name}-%{version}-no-read-0.patch

BuildArch:      noarch
BuildRequires:  python-setuptools-devel
BuildRequires:  python-nose

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It uses the 
pre-fork worker model, ported from Ruby's Unicorn project. It supports WSGI, 
Django, and Paster applications.

%prep
%setup -q
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test

%files
%doc LICENSE NOTICE README.rst THANKS
%{python_sitelib}/%{name}*
%{_bindir}/%{name}
%{_bindir}/%{name}_django
%{_bindir}/%{name}_paster

%changelog
* Tue Jan 31 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-2
- patch for failing test (gunicorn issue #294)

* Mon Jan 30 2012 Dan Callaghan <dcallagh@redhat.com> - 0.13.4-1
- initial version
