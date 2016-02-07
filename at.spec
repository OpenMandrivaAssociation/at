%define	debug_package %nil

Summary:	Job spooling tools
Name:		at
Version:	3.1.16
Release:	4
License:	GPLv2+
Group:		System/Servers
Url:		http://anonscm.debian.org/gitweb/?p=collab-maint/at.git
Source0:	http://ftp.debian.org/debian/pool/main/a/at/at_%{version}.orig.tar.gz
Source2:	pam.atd
Source3:	atd.sysconfig
Source4:	atd.service
Patch3:		at-3.1.7-sigchld.patch
Patch4:		at-3.1.13-noroot.patch
Patch9:		at-3.1.8-shell.patch
Patch10:	at-3.1.14-parallel-build.patch

BuildRequires:	bison
BuildRequires:	cronie
BuildRequires:	flex-devel
BuildRequires:	python
BuildRequires:	sendmail-command
BuildRequires:	pam-devel
BuildRequires: 	pkgconfig(libsystemd-login)
BuildRequires: 	pkgconfig(systemd)
Requires:	common-licenses
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

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
%patch3 -p1 -b .sigchld
%patch4 -p0 -b .noroot
%patch9 -p0 -b .shell
%patch10 -p0 -b .parallel
autoreconf -fiv

%build
%serverbuild_hardened

%configure \
	--with-loadavg_mx=1.5 \
	--with-atspool=%{_localstatedir}/spool/at/spool \
	--with-jobdir=%{_localstatedir}/spool/at

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

%files
%doc ChangeLog Problems README Copyright timespec
%attr(0644,daemon,daemon) %config(noreplace) %{_sysconfdir}/at.deny
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/atd

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
