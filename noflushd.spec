Summary:	Daemon that sends idle disks to sleep
Summary(pl):	Demon usypiaj±cy bezczynne dyski
Name:		noflushd
Version:	2.7.5
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/noflushd/%{name}_%{version}.orig.tar.gz
# Source0-md5:	a1712430588650bb8f99c5b5f2ce2511
# init script based on file distributed with sources
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://noflushd.sf.net/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
noflushd is a simple daemon that monitors disk activity and spins down
disks whose idle time exceeds a certain timeout. It requires a kernel
thread named kupdate which is present in Linux kernel version 2.2.11
and later or pdflush for 2.6 kernels. For earlier kernels, bdflush
version 1.6 provides equal functionality.

%description -l pl
noflushd jest prostym demonem monitoruj±cym aktywno¶æ dysków i
zatrzymuj±cym te dyski, których czas bezczynno¶ci przekroczy³
okre¶lony limit. Wymaga w±tku j±dra o nazwie kupdate, wystêpuj±cego
od wersji 2.2.11, lub pdflush dla j±der 2.6. Dla wcze¶niejszych
j±der program bdflush w wersji 1.6 zapewnia t± sam± funkcjonalno¶æ.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add noflushd
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "NOTE: Edit /etc/sysconfig/noflushd to configure %{name}."
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_sbindir}/noflushd
%attr(754,root,root) /etc/rc.d/init.d/noflushd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man8/noflushd.8*
