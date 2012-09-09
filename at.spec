Summary:	Job spooling tools
Name:		at
Version:	3.1.13
Release:	4
License:	GPL
Group:		System/Servers
Url:		http://qa.mandriva.com
Source0:	http://ftp.debian.org/debian/pool/main/a/at/at_%{version}.orig.tar.gz
Source1:	atd.init
Source2:	pam.atd
Source3:	atd.sysconfig
Source4:	atd.service
Patch3:		at-3.1.7-sigchld.patch
Patch9:		at-3.1.8-shell.patch
Patch11:	at-3.1.13-makefile.patch
Requires(post):	coreutils chkconfig /etc/init.d rpm-helper systemd-units
Requires(preun):	coreutils chkconfig /etc/init.d rpm-helper systemd-units
Conflicts:	crontabs <= 1.5
Requires:	common-licenses
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	python
BuildRequires:	sendmail-command
BuildRequires:	bison
BuildRequires:	vixie-cron
BuildRequires:	pam-devel
BuildRequires:	systemd-units

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
%patch9 -p0 -b .shell
%patch11 -p1 -b .makefile

%build
autoreconf -fi
%if %mdvver >= 201200
%serverbuild_hardened
%else
%serverbuild
%endif

%configure2_5x \
	--with-atspool=/var/spool/at/spool \
	--with-jobdir=/var/spool/at

%make

%install
mkdir -p %{buildroot}/{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

make install IROOT=%{buildroot} DAEMON_USERNAME=`id -nu` \
	DAEMON_GROUPNAME=`id -ng` \
    atdocdir=%{_docdir}/at

echo > %{buildroot}/%{_sysconfdir}/at.deny

mkdir -p %{buildroot}/%{_sysconfdir}/pam.d
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/pam.d/atd

install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/atd

%if %mdkver < 201200
mkdir -p %{buildroot}%{_initrddir}
cp -a %{SOURCE1} %{buildroot}%{_initrddir}/atd
chmod 755 %{buildroot}%{_initrddir}/atd
%else
#(tpg) install systemd initscript
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/atd.service
%endif

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

%if %mdkver < 201200
%{_initrddir}/atd
%else
%attr(0644,root,root) %{_unitdir}/atd.service
%endif

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
