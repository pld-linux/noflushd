Summary:	Daemon that sends idle disks to sleep
Summary(pl):	Demon usypiaj±cy bezczynne dyski
Name:		noflushd
Version:	2.6.1
Release:	1
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/noflushd/%{name}_%{version}.orig.tar.gz
URL:		http://noflushd.sf.net/
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig

%define		_sbindir	/sbin

%description
noflushd is a simple daemon that monitors disk activity and spins down
disks whose idle time exceeds a certain timeout. It requires a kernel
thread named kupdate which is present in Linux kernel version 2.2.11
and later. For earlier kernels, bdflush version 1.6 provides equal
functionality.

%description -l pl
noflushd jest prostym demonem monitoruj±cym aktywno¶æ dysków i
zatrzymuj±cym te dyski, których czas bezczynno¶ci przekroczy³
okre¶lony limit. Wymaga w±tku kernela o nazwie kupdate - wystêpuj±cym
od wersji 2.2.11. Dla wcze¶niejszych kerneli program bdflush w wersji
1.6 zapewnia t± sam± funkcjonalno¶æ.

%prep
%setup -q

%build
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add noflushd
echo "NOTE: Edit /etc/rc.d/init.d/noflushd to set the default timeout (1h)."

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del noflushd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_sbindir}/noflushd
%attr(754,root,root) /etc/rc.d/init.d/noflushd
%{_mandir}/man8/noflushd.8*
