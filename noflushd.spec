Summary:	Daemon that sends idle disks to sleep
Summary(pl):	Demon usypiaj±cy bezczynne dyski
Name:		noflushd
Version:	1.8.3
Release:	1
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	%{name}_%{version}-1.tar.gz
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
noflushd is a simple daemon that monitors disk activity and spins down
disks whose idle time exceeds a certain timeout. It requires a kernel
thread named kupdate which is present in Linux kernel version 2.2.11
and later. For earlier kernels, bdflush version 1.6 provides equal
functionality.

%prep
%setup -q -n noflushd-%{version}

%build
%{__make} USER_CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0750 $RPM_BUILD_ROOT/etc/rc.d/init.d
%{__make} INSTALL_PREFIX=$RPM_BUILD_ROOT/ \
	RCDIR=$RPM_BUILD_ROOT/etc/rc.d/init.d generic_install
[ ! -d $RPM_BUILD_ROOT/var/adm/fillup-templates ] && \
	install -d -m 755 $RPM_BUILD_ROOT/var/adm/fillup-templates
install skripts/rc.config.noflushd $RPM_BUILD_ROOT/var/adm/fillup-templates/rc.config.noflushd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%chkconfig_add
echo "NOTE: Edit /etc/rc.d/init.d/noflushd to set the default timeout (1h)."

%preun
%chkconfig_del

%files
%defattr(644,root,root,755)
%doc README ChangeLog contrib/
%attr(755,root,root) /sbin/noflushd
%attr(754,root,root) /etc/rc.d/init.d/noflushd
%{_mandir}/man8/noflushd.8
/var/adm/fillup-templates/rc.config.noflushd
