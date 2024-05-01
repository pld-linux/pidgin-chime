#
# Conditional build:
%bcond_without	evolution	# Evolution plugin

Summary:	Pidgin plugin for Amazon Chime
Summary(pl.UTF-8):	Wtyczka Pidgina do komunikatora Amazon Chime
Name:		pidgin-chime
Version:	1.4.1
Release:	2
License:	LGPL v2.1
Group:		Applications/Communication
#Source0:	ftp://ftp.infradead.org/pub/pidgin-chime/%{name}-%{version}.tar.gz
Source0:	https://github.com/awslabs/pidgin-chime/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6c312bba0521c4bce4c2d7dcb82d8a36
URL:		https://github.com/awslabs/pidgin-chime
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
%if %{with evolution}
BuildRequires:	evolution-data-server-devel >= 3.33.2
BuildRequires:	evolution-devel >= 3.33.2
%endif
BuildRequires:	farstream-devel >= 0.2
BuildRequires:	gettext-tools
BuildRequires:	gnutls-devel >= 3.2.0
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	json-glib-devel
BuildRequires:	libmarkdown-devel
BuildRequires:	libpurple-devel >= 2.8.0
BuildRequires:	libsoup-devel >= 2.59
BuildRequires:	libtool >= 2:2
BuildRequires:	libxcb-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	opus-devel
BuildRequires:	pidgin-devel >= 2.13.0
BuildRequires:	pkgconfig
BuildRequires:	protobuf-c-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
Requires:	libpurple-protocol-chime = %{version}-%{release}
Requires:	pidgin >= 2.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A plugin for the Pidgin multi-protocol instant messenger, to support
Amazon Chime.

This package provides the icon set for Pidgin, and a UI plugin to
indicate seen messages.

%description -l pl.UTF-8
Wtyczka wieloprotokołowego komunikatora Pidgin, pozwalająca na obsługę
protokołu Amazon Chime.

Ten pakiet dostarcza zestaw ikon dla Pidgina oraz wtyczkę interfejsu
użytkownika do oznaczania widzianych wiadomości.

%package -n libpurple-protocol-chime
Summary:	Libpurple protocol plugin for Amazon Chime
Summary(pl.UTF-8):	Wtyczka protokołu libpurple dla komunikatora Amazon Chime
Group:		Libraries
Requires:	gnutls-libs >= 3.2.0
Requires:	libpurple >= 2.8.0
Requires:	libsoup >= 2.59

%description -n libpurple-protocol-chime
This package provides the Amazon Chime protocol support for the
libpurple messaging library, which is used by Pidgin and other tools.

%description -n libpurple-protocol-chime -l pl.UTF-8
Ten pakiet zapewnia obsługę protokołu Amazon Chime dla biblioteki
komunikacyjnej libpurple, używanej przez Pidgina i inne narzędzia.

%package -n evolution-chime
Summary:	Evolution plugin for Amazon Chime
Summary(pl.UTF-8):	Wtyczka Evolution dla komunikatora Amazon Chime
Group:		Applications/Communication
Requires:	evolution >= 3.33.2
Requires:	evolution-data-server >= 3.33.2
Requires:	libpurple-protocol-chime = %{version}-%{release}

%description -n evolution-chime
A plugin for Evolution that allows you to create meetings in Amazon
Chime.

%description -n evolution-chime -l pl.UTF-8
Wtyczka Evolution umożliwiająca tworzenie spotkań w Amazon Chime.

%prep
%setup -q

%build
# rebuild for as-needed to work
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_evolution:--without-evolution}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/farstream-0.2/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pidgin/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/purple-2/*.la
%if %{with evolution}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/evolution/modules/*.la
%endif

# only single empty file exists
#find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/chime-auth.py
%attr(755,root,root) %{_bindir}/chime-joinable.py
%attr(755,root,root) %{_libdir}/pidgin/chimeseen.so
%{_desktopdir}/chime-auth.desktop
%{_pixmapsdir}/pidgin/protocols/*/chime.png
%{_pixmapsdir}/pidgin/protocols/scalable/chime*.svg

%files -n libpurple-protocol-chime
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/farstream-0.2/libapp-transmitter.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstchime.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstxcbimagesrc.so
%attr(755,root,root) %{_libdir}/purple-2/libchimeprpl.so
%{_datadir}/pidgin-chime

%files -n evolution-chime
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/evolution/modules/module-event-from-template.so
