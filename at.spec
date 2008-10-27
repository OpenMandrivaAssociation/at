Summary:	Job spooling tools
Name:		at
Version:	3.1.10.1
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
Source0:	http://ftp.debian.org/debian/pool/main/a/at/at_%{version}.tar.gz
Url:		http://qa.mandriva.com
Source1:	atd.init
Source2:    pam.atd
Patch0:		at-3.1.7-lockfile.patch
Patch3:		at-3.1.7-sigchld.patch
Patch4:		at-3.1.8-noroot.patch
Patch5:		at-3.1.8-typo.patch
Patch9:		at-3.1.8-shell.patch
Requires(post):	coreutils chkconfig /etc/init.d rpm-helper
Requires(preun):  coreutils chkconfig /etc/init.d rpm-helper
Conflicts:	crontabs <= 1.5
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	common-licenses
BuildRequires:	autoconf2.1 automake1.7 flex gcc python sendmail-command
BuildRequires:	bison vixie-cron
BuildRequires:  pam-devel

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
%patch0 -p1 -b .lockfile
%patch3 -p1 -b .sigchld
%patch4 -p0 -b .noroot
%patch5 -p1 -b .tyop
%patch9 -p0 -b .shell

export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf

%build
%serverbuild
%configure --with-atspool=/var/spool/at/spool --with-jobdir=/var/spool/at

%make

%install
rm -rf $RPM_BUILD_ROOT 
mkdir -p $RPM_BUILD_ROOT/{%{_initrddir},%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

make install IROOT=$RPM_BUILD_ROOT DAEMON_USERNAME=`id -nu` \
	DAEMON_GROUPNAME=`id -ng` \
    atdocdir=%_docdir/at

echo > $RPM_BUILD_ROOT/%{_sysconfdir}/at.deny
%{__cp} -a %{SOURCE1} %{buildroot}%{_initrddir}/atd
chmod 755 $RPM_BUILD_ROOT%{_initrddir}/atd

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d
install -m 644 %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/atd

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/spool/at/.SEQ
chmod 660 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ

%_post_service atd

%preun
%_preun_service atd

%files
%defattr(-,root,root)
%doc ChangeLog Problems README Copyright timespec
%attr(0640,root,daemon) %config(noreplace) %{_sysconfdir}/at.deny
%{_initrddir}/atd
%{_sysconfdir}/pam.d/atd
%attr(0770,daemon,daemon)	%dir /var/spool/at
%attr(0660,daemon,daemon)	%verify(not md5 size mtime) %ghost /var/spool/at/.SEQ
%attr(0770,daemon,daemon)	%dir /var/spool/at/spool
%{_sbindir}/atrun
%{_sbindir}/atd
%attr(6755,daemon,daemon) %{_bindir}/batch
%attr(6755,daemon,daemon) %{_bindir}/atrm
%attr(6755,daemon,daemon)   %{_bindir}/at
%{_bindir}/atq
%{_mandir}/*/atrun.8*
%{_mandir}/*/atd.8*
%{_mandir}/*/at.1*
%{_mandir}/*/atq.1*
%{_mandir}/*/atrm.1*
%{_mandir}/*/batch.1*
%{_mandir}/*/at_allow.5*
%{_mandir}/*/at_deny.5*
