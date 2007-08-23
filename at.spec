Summary:	Job spooling tools
Name:		at
Version:	3.1.8
Release:	%mkrel 22
License:	GPL
Group:		System/Servers
Source0:	ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/at-3.1.8.tar.bz2
Url:		http://qa.mandriva.com
Source1:	atd.init
Patch0:		at-3.1.7-lockfile.patch
#Patch1:	at-3.1.7-noon.patch
Patch2:		at-3.1.7-paths.patch
Patch3:		at-3.1.7-sigchld.patch
Patch4:		at-3.1.8-noroot.patch
Patch5:		at-3.1.8-typo.patch
Patch6:		at-3.1.8-debian.patch
Patch7:		at-3.1.8-buflen.patch
Patch8:		at-3.1.8-UTC.patch
Patch9:		at-3.1.8-shell.patch
Patch10:	at-3.1.8-o_excl.patch
Patch11:	at-3.1.8-heapcorruption.patch
Patch12:        at-3.1.8-no-strip-shell-script.patch
Requires(post):	coreutils chkconfig /etc/init.d rpm-helper
Requires(preun):  coreutils chkconfig /etc/init.d rpm-helper
Conflicts:	crontabs <= 1.5
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	common-licenses
BuildRequires:	autoconf2.1 automake1.7 flex gcc python sendmail-command
BuildRequires:	bison vixie-cron

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
# The next path is a brute-force fix that will have to be updated
# when new versions of at are released.
%patch2 -p1 -b .paths

%patch3 -p1 -b .sigchld
%patch6 -p0 -b .debian
%patch4 -p1 -b .noroot
%patch5 -p1 -b .tyop
%patch7 -p1 -b .buflen
%patch8 -p1
%patch9 -p1 -b .shell
%patch10 -p1 -b .o_excl
%patch11 -p1 -b .heapcorruption
%patch12 -p1 -b .no-strip-shell-script

#cat /usr/share/aclocal/libtool.m4 >> aclocal.m4
#libtoolize --force
#aclocal-1.7
#WANT_AUTOCONF_2_5=1 autoconf-2.5x

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
	DAEMON_GROUPNAME=`id -ng`
	# \
	#etcdir=$RPM_BUILD_ROOT/etc \
	#ATJOB_DIR=$RPM_BUILD_ROOT/var/spool/at \
	#ATSPOOL_DIR=$RPM_BUILD_ROOT/var/spool/at/spool 
echo > $RPM_BUILD_ROOT/%{_sysconfdir}/at.deny
%{__cp} -a %{SOURCE1} %{buildroot}%{_initrddir}/atd
#install -m 755 $RPM_SOURCE_DIR/atd.init 
chmod 755 $RPM_BUILD_ROOT%{_initrddir}/atd

#(peroyvind) remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/at_allow.5

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/spool/at/.SEQ
chmod 600 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ

%_post_service atd

%preun
%_preun_service atd

%files
%defattr(-,root,root)
%doc ChangeLog Problems README Copyright timespec
%config(noreplace) %{_sysconfdir}/at.deny
%{_initrddir}/atd
%attr(0700,daemon,daemon)	%dir /var/spool/at
%attr(0600,daemon,daemon)	%verify(not md5 size mtime) %ghost /var/spool/at/.SEQ
%attr(0700,daemon,daemon)	%dir /var/spool/at/spool
%{_sbindir}/atrun
%{_sbindir}/atd
%{_mandir}/*/atrun.8*
%{_mandir}/*/atd.8*
%{_mandir}/*/at.1*
%{_mandir}/*/atq.1*
%{_mandir}/*/atrm.1*
%{_mandir}/*/batch.1*
%{_bindir}/batch
%{_bindir}/atrm
%{_bindir}/atq

%attr(4755,root,root)   %{_bindir}/at


