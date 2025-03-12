#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests (require DISPLAY)

%define		module	pygobject
Summary:	Python 3 bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki GObject
Name:		python3-pygobject3
Version:	3.52.1
Release:	1
License:	LGPL v2+
Group:		Libraries/Python
Source0:	https://download.gnome.org/sources/pygobject/3.52/%{module}-%{version}.tar.gz
# Source0-md5:	123f69218036939f216593fdc1ee0799
URL:		https://pygobject.gnome.org/
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.80.0
BuildRequires:	gobject-introspection-devel >= 1.64.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-pycairo-devel >= 1.16.0
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov >= 1:4.13
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
%if %{with doc}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton >= 0.5.2
BuildRequires:	python3-pydata_sphinx_theme
%endif
Requires:	glib2 >= 1:2.80.0
Requires:	gobject-introspection >= 1.64.0
Requires:	python3-modules >= 1:3.9
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
Requires:	glib2-devel >= 1:2.80.0
Requires:	libffi-devel >= 3.0
Requires:	python3-devel >= 1:3.9
Obsoletes:	python3-pygobject3-examples < 3.50

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
Requires:	glib2-devel >= 1:2.80.0
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

%prep
%setup -q -n %{module}-%{version}

%build
%meson \
	-Dpycairo=enabled \
	%{!?with_tests:-Dtests=false}

%meson_build

%if %{with doc}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py3_sitescriptdir}/gi/overrides/__pycache__

%meson_install

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

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
%{py3_sitedir}/PyGObject-%{version}.dist-info
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
