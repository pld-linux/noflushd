%define	version	1.8.3

Summary: Daemon that sends idle disks to sleep
Name: noflushd
Version: %{version}
Release: 1
Copyright: GPL
Group: System Environment/Daemons
Source0: noflushd_%{version}-1.tar.gz

Buildroot:	/tmp/noflushd.rpmbuild
%changelog

* Mon Mar 13 2000 Daniel Kobras <kobras@linux.de>

  Release 1.8.3-1:

- New upstream version

* Mon Feb  7 2000 Daniel Kobras <kobras@linux.de>

  Release 1.8.2-1:

- New upstream version

* Thu Jan 27 2000 Daniel Kobras <kobras@linux.de>

  Release 1.8.1-1:

- New upstream version

* Tue Jan 25 2000 Daniel Kobras <kobras@linux.de>

  Release 1.8-1:

- New upstream version

* Sat Sep 04 1999 Daniel Kobras <kobras@linux.de>

  Release 1.7.4-1:

- Merged RedHat and SuSE specs

* Fri Aug 27 1999 Daniel Kobras <kobras@linux.de>

  Release 1.7.3-1:

- Fixed several minor bugs in spec file

* Wed Aug 25 1999 Daniel Kobras <kobras@linux.de>

  Release 1.7.2-1:

- Added RPM spec file stuff

%description
noflushd is a simple daemon that monitors disk activity and spins down
disks whose idle time exceeds a certain timeout. It requires a kernel thread
named kupdate which is present in Linux kernel version 2.2.11 and later. For
earlier kernels, bdflush version 1.6 provides equal functionality.

%prep
%setup -n noflushd-%{version}

%build
make USER_CFLAGS="$RPM_OPT_FLAGS"

%install
install -d -o root -g root -m 0750 $RPM_BUILD_ROOT/etc/rc.d/init.d
make INSTALL_PREFIX=$RPM_BUILD_ROOT/ \
     RCDIR=$RPM_BUILD_ROOT/etc/rc.d/init.d generic_install
[ ! -d $RPM_BUILD_ROOT/var/adm/fillup-templates ] && \
 install -d -o root -g root -m 755 $RPM_BUILD_ROOT/var/adm/fillup-templates
install -m 644 skripts/rc.config.noflushd $RPM_BUILD_ROOT/var/adm/fillup-templates/rc.config.noflushd
%post
echo "Updating startup files..."
# SuSE init sucks. They have this rctab helper, but it's only for
# interactive use and error recovery.
if [ -d sbin/init.d ]; then \
	for i in 1 2 3; do \
		ln -sf ../noflushd sbin/init.d/rc$i.d/S80noflushd; \
		ln -sf ../noflushd sbin/init.d/rc$i.d/K10noflushd; \
	done; \
	if [ -x bin/fillup ]; then \
		bin/fillup -q -d = etc/rc.config var/adm/fillup-templates/rc.config.noflushd	
		echo "NOTE: Default timeout is 1 hour."; \
		echo "      Edit NOFLUSHD_TIMEOUT in /etc/rc.config to change."; \
	else \
		echo "NOTE: fillup not found. rc.config unchanged."; \
		echo "      Edit /sbin/init.d/noflushd to set the default timeout (1h)."; \
	fi; \
else \
if [ -x /sbin/chkconfig ]; then \
	/sbin/chkconfig --add noflushd; \
else \
	echo "ERROR: Could not include noflushd in system startup. Please update"; \
	echo "       your system by hand."; \
fi; \
echo "NOTE: Edit /etc/rc.d/init.d/noflushd to set the default timeout (1h)."; \
fi
%preun
if [ -d /sbin/init.d ]; then \
	for i in /sbin/init.d/rc?.d; do \
		rm -f $i/*noflushd; \
	done; \
else \	
if [ -x /sbin/chkconfig ]; then \
	/sbin/chkconfig --del noflushd; \
fi; \
fi
%files
%doc	README
%doc	COPYING
%doc	ChangeLog
%doc	contrib/
	/sbin/noflushd
	/etc/rc.d/init.d/noflushd
	/usr/man/man8/noflushd.8
	/var/adm/fillup-templates/rc.config.noflushd
