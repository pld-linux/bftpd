Summary:	Small FTP server
Summary(pl):	Ma³y serwer FTP
Name:		bftpd
Version:	1.0.18
Release:	1
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://www.bftpd.f2s.com/downloads/src/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.conf
Patch0:		%{name}-NOROOT.patch
Requires:	inetdaemon
Prereq:		rc-inetd
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	wu-ftpd
Obsoletes:	anonftp
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	proftpd
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd

%description
bftpd is a Linux FTP server with chroot and setreuid. Not all FTP
commands are included. It doesn't need special home directory
preparation and accesses either the user's home directory or its .ftp
subdirectory, and user authentication is via passwd/shadow or PAM.

%description -l pl
bftpd jest linuksowym serwerem FTP z chroot i setreuid. Nie wszystkie
komdeny FTP s± dostêpne. Nie wymaga specjalnego katalogu domowego i
dostêpu poza katalogiem domowym u¿ytkownika i podkatalogiem .ftp.
Autoryzacja u¿ytkowników poprzez passwd/shadow lub PAM.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_prefix}{/sbin,/share/man/man8},/etc/sysconfig/rc-inetd,/home/ftp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/ftp
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/ftpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf README CHANGELOG

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
#%attr(640,root,root) /etc/pam.d/ftp
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config /etc/sysconfig/rc-inetd/ftpd
%dir %attr(555,ftp,ftp) /home/ftp

%{_mandir}/man8/*
