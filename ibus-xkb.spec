#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	gnomekbd	# libgnomekbd support
%bcond_without	dconf		# dconf-based configuration
%bcond_without	gconf		# GConf support
#
Summary:	XKB module for IBus
Summary(pl.UTF-8):	Moduł XKB dla platformy IBus
Name:		ibus-xkb
Version:	1.4.99.20120525
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: http://code.google.com/p/ibus/downloads/list
Source0:	http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	c29db74b3add447f58a1bed2d4d55138
URL:		http://code.google.com/p/ibus/
%{?with_gconf:BuildRequires:	GConf2-devel >= 2.12}
%{?with_gnomekbd:BuildRequires:	atk-devel}
%{?with_dconf:BuildRequires:	dconf-devel >= 0.7.5}
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.6.8
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	ibus-devel >= 1.4.99
BuildRequires:	intltool >= 0.35.0
%{?with_gnomekbd:BuildRequires:	libgnomekbd-devel}
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	vala >= 2:0.14
BuildRequires:	vala-ibus >= 1.4.99
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libxkbfile-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ibus >= 1.4.99
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/ibus

%description
XKB module for IBus.

%description -l pl.UTF-8
Moduł XKB dla platformy IBus.

%package libs
Summary:	Shared ibus-xkb library
Summary(pl.UTF-8):	Biblioteka współdzielona ibus-xkb
Group:		Libraries
Requires:	glib2 >= 1:2.26.0
Requires:	ibus-libs >= 1.4.99

%description libs
Shared ibus-xkb library.

%description libs -l pl.UTF-8
Biblioteka współdzielona ibus-xkb.

%package devel
Summary:	Development files for ibus-xkb library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki ibus-xkb
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
Requires:	ibus-devel >= 1.4.99

%description devel
Development files for ibus-xkb library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki ibus-xkb.

%package static
Summary:	Static ibus-xkb library
Summary(pl.UTF-8):	Statyczna biblioteka ibus-xkb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ibus-xkb library.

%description static -l pl.UTF-8
Statyczna biblioteka ibus-xkb.

%package -n vala-ibus-xkb
Summary:	Vala API for ibus-xkb library
Summary(pl.UTF-8):	API języka Vala dla biblioteki ibus-xkb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.14
Requires:	vala-ibus >= 1.4.99

%description -n vala-ibus-xkb
Vala API for ibus-xkb library.

%description -n vala-ibus-xkb -l pl.UTF-8
API języka Vala dla biblioteki ibus-xkb.

%prep
%setup -q

%build
%configure \
	%{?with_dconf:--enable-dconf} \
	%{!?with_gconf:--disable-gconf} \
	%{!?with_gnomekbd:--disable-libgnomekbd} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libibus-xkb-1.0.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with gconf}
%gconf_schema_install ibus-xkb.schemas
%endif
%if %{with dconf}
%glib_compile_schemas
%endif

%if %{with gconf}
%preun
%gconf_schema_uninstall ibus-xkb.schemas
%endif

%if %{with dconf}
%postun
%glib_compile_schemas
%endif

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/ibus-setup-xkb
%attr(755,root,root) %{_libexecdir}/ibus-engine-xkb
%attr(755,root,root) %{_libexecdir}/ibus-xkb
%attr(755,root,root) %{_libexecdir}/ibus-xkb-ui-gtk3
%{_datadir}/ibus/component/gtkxkbpanel.xml
%{_datadir}/ibus/component/xkb.xml
%{_datadir}/ibus/setup-xkb
%{_desktopdir}/ibus-setup-xkb.desktop
%{?with_gconf:%{_sysconfdir}/gconf/schemas/ibus-xkb.schemas}
%if %{with dconf}
%dir %{_sysconfdir}/dconf/db/ibus.d
%{_sysconfdir}/dconf/db/ibus.d/01-xkb
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.xkb.gschema.xml
%{_datadir}/GConf/gsettings/ibus-xkb.convert
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibus-xkb-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libibus-xkb-1.0.so.5
%{_libdir}/girepository-1.0/IBusXKB-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibus-xkb-1.0.so
%{_includedir}/ibus-xkb-1.0
%{_datadir}/gir-1.0/IBusXKB-1.0.gir
%{_pkgconfigdir}/ibus-xkb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libibus-xkb-1.0.a
%endif

%files -n vala-ibus-xkb
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/ibus-xkb-1.0.deps
%{_datadir}/vala/vapi/ibus-xkb-1.0.vapi
