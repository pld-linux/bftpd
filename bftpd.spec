Summary:	Small FTP server
Summary(pl):	Ma³y serwer FTP
Name:		bftpd
Version:	1.0.22
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://bftpd.sourceforge.net/downloads/src/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.conf
Source3:	ftpusers.tar.bz2
URL:		http://www.bftpd.org/
Patch0:		%{name}-NOROOT.patch
BuildRequires:	autoconf
Requires:	inetdaemon
Prereq:		rc-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
Conflicts:	man-pages < 1.51

%description
bftpd is a Linux FTP server with chroot and setreuid. Not all FTP
commands are included. It doesn't need special home directory
preparation and accesses either the user's home directory or its .ftp
subdirectory, and user authentication is via passwd/shadow or PAM.

%description -l pl
bftpd jest linuksowym serwerem FTP z chroot i setreuid. Nie wszystkie
komendy FTP s± dostêpne. Nie wymaga specjalnego katalogu domowego i
dostêpu poza katalogiem domowym u¿ytkownika i podkatalogiem .ftp.
Autoryzacja u¿ytkowników poprzez passwd/shadow lub PAM.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_prefix}{/sbin,/share/man/man8},/etc/sysconfig/rc-inetd,/home/services/ftp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/ftp
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/ftpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG
%doc %lang(en) doc/en/*.{html,txt}
%doc %lang(pl) doc/pl/*.{html,txt}
%attr(755,root,root) %{_sbindir}/*
#%attr(640,root,root) /etc/pam.d/ftp
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config /etc/sysconfig/rc-inetd/ftpd
%dir %attr(555,ftp,ftp) /home/services/ftp

%{_mandir}/man8/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
