Summary:	Job spooling tools
Name:		at
Version:	3.1.13
Release:	8
License:	GPLv2+
Group:		System/Servers
Url:		http://qa.mandriva.com
Source0:	http://ftp.debian.org/debian/pool/main/a/at/at_%{version}.orig.tar.gz
Source2:	pam.atd
Source3:	atd.sysconfig
Source4:	atd.service
Patch3:		at-3.1.7-sigchld.patch
Patch9:		at-3.1.8-shell.patch
Patch11:	at-3.1.13-makefile.patch
Requires(post):	coreutils rpm-helper systemd-units
Requires(preun):coreutils rpm-helper systemd-units
Conflicts:	crontabs <= 1.5
Requires:	common-licenses
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	python
BuildRequires:	sendmail-command
BuildRequires:	bison
BuildRequires:	cronie
BuildRequires:	pam-devel
BuildRequires:	systemd-units
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(systemd)

%description
At and batch read commands from standard input or from a specified file.
At allows you to specify that a command will be run at a particular time
(now or a specified time in the future).  Batch will execute commands
when the system load levels drop to a particular level.  Both commands
use /bin/sh to run the commands.

You should install the at package if you need a utility that will do
time-oriented job control.  Note: you should use crontab instead, if it is
a recurring job that will need to be repeated at the same time every
day/week/etc.

%prep
%setup -q
%patch3 -p1 -b .sigchld~
%patch9 -p0 -b .shell~
%patch11 -p1 -b .makefile~
autoreconf -fi

%build
%serverbuild_hardened

%configure2_5x \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at

%make

%install
mkdir -p %{buildroot}{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

make install IROOT=%{buildroot} DAEMON_USERNAME=`id -nu` \
	DAEMON_GROUPNAME=`id -ng` \
    atdocdir=%{_docdir}/at

touch %{buildroot}%{_sysconfdir}/at.deny

install -p -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/pam.d/atd

install -p -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/sysconfig/atd

#(tpg) install systemd initscript
install -p -m644 %{SOURCE4} -D %{buildroot}%{_unitdir}/atd.service

%post
touch /var/spool/at/.SEQ
chmod 660 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ

if [ "$1" = "1" ]; then
 /bin/systemctl enable atd.service >/dev/null 2>&1 || :
fi

%_post_service atd

%preun
%_preun_service atd

%files
%doc ChangeLog Problems README Copyright timespec
%attr(0640,root,daemon) %config(noreplace) %{_sysconfdir}/at.deny
%config(noreplace) %{_sysconfdir}/sysconfig/atd

%attr(0644,root,root) %{_unitdir}/atd.service

%{_sysconfdir}/pam.d/atd
%attr(0770,daemon,daemon) %dir /var/spool/at
%attr(0660,daemon,daemon) %verify(not md5 size mtime) %ghost /var/spool/at/.SEQ
%attr(0770,daemon,daemon) %dir /var/spool/at/spool
%{_sbindir}/atrun
%{_sbindir}/atd
%attr(6755,daemon,daemon) %{_bindir}/batch
%attr(6755,daemon,daemon) %{_bindir}/atrm
%attr(6755,daemon,daemon) %{_bindir}/at
%{_bindir}/atq
%{_mandir}/*/atrun.8*
%{_mandir}/*/atd.8*
%{_mandir}/*/at.1*
%{_mandir}/*/atq.1*
%{_mandir}/*/atrm.1*
%{_mandir}/*/batch.1*
%{_mandir}/*/at.allow.5*
%{_mandir}/*/at.deny.5*

%changelog
* Fri Dec 14 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.1.13-8
- update license with version
- cleanup a bit
- do autoreconf in %prep

* Sun Sep 09 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.13-4
+ Revision: 816601
- install only systemd service for mdv 2012
- pass correct options in service file
- spec file clean

* Sun Jan 15 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.13-3
+ Revision: 760977
- add systemd support

* Sun Oct 02 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.13-2
+ Revision: 702406
- use %%serverbuild_hardened flags for mdv2012

* Tue Sep 13 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 3.1.13-1
+ Revision: 699585
- update to new version 3.1.13
- merge patches 4 and 10 into new patch 11
- enable LDFLAGS in patch 11

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.1.12-4
+ Revision: 662883
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1.12-3mdv2011.0
+ Revision: 603475
- rebuild

* Mon Dec 07 2009 Pascal Terjan <pterjan@mandriva.org> 3.1.12-2mdv2010.1
+ Revision: 474425
- Fix parallel build

  + Funda Wang <fwang@mandriva.org>
    - use configure2_5x

* Mon Dec 07 2009 Olivier Thauvin <nanardon@mandriva.org> 3.1.12-1mdv2010.1
+ Revision: 474339
- 3.1.12

* Fri Nov 13 2009 Olivier Thauvin <nanardon@mandriva.org> 3.1.11-3mdv2010.1
+ Revision: 465896
- 3.1.11, remove merged patch

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.1.10.2-3mdv2010.0
+ Revision: 424370
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sun Feb 22 2009 Olivier Thauvin <nanardon@mandriva.org> 3.1.10.2-1mdv2009.1
+ Revision: 344001
- 3.1.10.2

* Sat Dec 13 2008 Olivier Thauvin <nanardon@mandriva.org> 3.1.10.1-3mdv2009.1
+ Revision: 313901
- make the load under which batch job are launch configurable, default is now N CPUs - 0.2

* Mon Oct 27 2008 Olivier Thauvin <nanardon@mandriva.org> 3.1.10.1-2mdv2009.1
+ Revision: 297720
- use pam
- fix #45066: eg make at usuable again for non root users

* Fri Aug 15 2008 Olivier Thauvin <nanardon@mandriva.org> 3.1.10.1-1mdv2009.0
+ Revision: 272478
- 3.1.10.1

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 3.1.8-25mdv2009.0
+ Revision: 220463
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 3.1.8-24mdv2008.1
+ Revision: 148875
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 3.1.8-23mdv2008.0
+ Revision: 69909
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 3.1.8-22mdv2008.0
+ Revision: 45082
- rebuild with new serverbuild macro (-fstack-protector-all)

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild with correct optflags


* Sat Jan 06 2007 David Walluck <walluck@mandriva.org> 3.1.8-20mdv2007.0
+ Revision: 104958
- rebuild
  bunzip2 patches
  fix install
- Import at

* Sat May 13 2006 Stefan van der Eijk <stefan@eijk.nu> 3.1.8-19mdk
- rebuild for sparc

* Sun Jan 08 2006 Olivier Blin <oblin@mandriva.com> 3.1.8-18mdk
- convert parallel init to LSB

* Sat Dec 31 2005 Couriousous <couriousous@mandriva.org> 3.1.8-17mdk
- Add parallel init stuff

* Fri Aug 19 2005 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 3.1.8-16mdk
- fix buildrequires

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 3.1.8-15mdk
- fix rpmlint errors (PreReq)

* Thu Aug 11 2005 Nicolas LÃ©cureuil <neoclust@mandriva.org> 3.1.8-14mdk
- fix rpmlint errors (PreReq)

* Wed Aug 10 2005 Warly <warly@mandriva.com> 3.1.8-13mdk
- change smtpdaemon require to sendmail-command

* Mon Jan 10 2005 Frederic Lepied <flepied@mandrakesoft.com> 3.1.8-12mdk
- BuildRequires vixie-cron for /var/spool/cron

* Thu Sep 09 2004 Pixel <pixel@mandrakesoft.com> 3.1.8-11mdk
- don't require "mailx" anymore 
  (otherwise we have at->mailx->smtpdaemon->postfix and postfix is installed by default)

* Wed Jun 09 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 3.1.8-10mdk
- fix buildrequires
- do parallell build

* Thu Jan 08 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.1.8-9mdk
- fix unpackaged files

