#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests (require DISPLAY)

%define		module	pygobject
Summary:	Python 3 bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki GObject
Name:		python3-pygobject3
Version:	3.42.2
Release:	2
License:	LGPL v2+
Group:		Libraries/Python
Source0:	https://download.gnome.org/sources/pygobject/3.42/%{module}-%{version}.tar.xz
# Source0-md5:	c5b31bb58156661c0954f1dbfc950fc9
URL:		https://wiki.gnome.org/Projects/PyGObject
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.56.0
BuildRequires:	gobject-introspection-devel >= 1.56.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-pycairo-devel >= 1.16.0
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
BuildRequires:	python3-sphinx_rtd_theme
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.56.0
Requires:	gobject-introspection >= 1.56.0
Requires:	python3-modules >= 1:3.6
Conflicts:	python3-pygobject < 2.28.6-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 3 bindings for GObject library.

%description -l pl.UTF-8
Wiązania Pythona 3 do biblioteki GObject.

%package devel
Summary:	Python 3 bindings for GObject library - development metapackage
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki GObject - metapakiet programistyczny
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3-common-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Requires:	libffi-devel >= 3.0
Requires:	python3-devel >= 1:3.5

%description devel
This metapackage gathers files required to develop GObject bindings
for Python 3.

%description devel -l pl.UTF-8
Ten metapakiet gromadzi pliki wymagane do tworzenia wiązań biblioteki
GObject dla Pythona 3.

%package -n python-pygobject3-common-devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Requires:	libffi-devel >= 3.0

%description -n python-pygobject3-common-devel
This package contains headers files required to build wrappers for
GObject addon libraries so that they interoperate with Python
bindings.

%description -n python-pygobject3-common-devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe wymagane do zbudowania funkcji do
biblioteki GObject, tak by mogły te biblioteki kooperowaći z
wiązaniami Pythona.

%package apidocs
Summary:	API documentation for Python GObject library
Summary(pl.UTF-8):	Dokumentacja biblioteki Pythona GObject
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python GObject library.

%description apidocs -l pl.UTF-8
Dokumentacja biblioteki Pythona GObject.

%package examples
Summary:	Example programs for GObject library
Summary(pl.UTF-8):	Programy przykładowe dla biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description examples
This package contains example programs for GObject library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy dla biblioteki GObject.

%prep
%setup -q -n %{module}-%{version}

%{__sed} -i -e '1s|#!/usr/bin/env python$|#!%{__python}|'  examples/cairo-demo.py

%build
%py3_build %{?with_tests:test}

%if %{with doc}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{py3_sitescriptdir}/gi/overrides/__pycache__}

%py3_install

cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README.rst
%dir %{py3_sitedir}/gi
%attr(755,root,root) %{py3_sitedir}/gi/_gi.cpython*.so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.cpython*.so
%{py3_sitedir}/gi/*.py
%{py3_sitedir}/gi/__pycache__
%dir %{py3_sitedir}/gi/overrides
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__
%dir %{py3_sitedir}/gi/repository
%{py3_sitedir}/gi/repository/*.py*
%{py3_sitedir}/gi/repository/__pycache__
%dir %{py3_sitedir}/pygtkcompat
%{py3_sitedir}/pygtkcompat/*.py
%{py3_sitedir}/pygtkcompat/__pycache__
%{py3_sitedir}/PyGObject-%{version}-py*.egg-info
%dir %{py3_sitescriptdir}/gi
%dir %{py3_sitescriptdir}/gi/overrides
%dir %{py3_sitescriptdir}/gi/overrides/__pycache__

%files devel
%defattr(644,root,root,755)

%files -n python-pygobject3-common-devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/{_images,_static,devguide,guide,*.html,*.js}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
