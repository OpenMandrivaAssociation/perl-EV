%define upstream_name    EV
%define upstream_version 4.15

%define filelist %{upstream_name}-%{upstream_version}-filelist
%define maketest 1

Name:      perl-%{upstream_name}
Version:   %perl_convert_version 4.15
Release:	1

Summary:   Wrapper for the libev high-performance event loop library
License:   Artistic
Group:     Development/Perl
Url:       http://software.schmorp.de/pkg/EV.html
Source0:   http://www.cpan.org/authors/id/M/ML/MLEHMANN/EV-4.15.tar.gz

BuildRequires: perl-devel
BuildRequires: perl-AnyEvent >= 1:2.6
BuildRequires: perl(common::sense)
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}

%description
A thin wrapper around libev, a high-performance event loop. Intended
as a faster and less buggy replacement for the Event perl
module. Efficiently supports very high number of timers, scalable
operating system APIs such as epoll, kqueue and solaris's ports,
child/pid watchers and more.

%prep
%setup -q -n %{upstream_name}-%{upstream_version} 
chmod -R u+w %{_builddir}/%{upstream_name}-%{upstream_version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
echo | %{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%{__make} 

%check
%{__make} test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%{perl_vendorarch}/EV.pm
%{perl_vendorarch}/EV
%{perl_vendorarch}/auto/EV
%_mandir/man3/EV*



%changelog
* Wed Jan 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.10.0-2
+ Revision: 768358
- svn commit -m mass rebuild of perl extension against perl 5.14.2

* Tue Dec 07 2010 Götz Waschk <waschk@mandriva.org> 4.10.0-1mdv2011.0
+ Revision: 613594
- update to new version 4.01

* Tue Jul 20 2010 Jérôme Quelin <jquelin@mandriva.org> 3.900.0-2mdv2011.0
+ Revision: 555809
- rebuild for perl 5.12

* Thu Dec 31 2009 Jérôme Quelin <jquelin@mandriva.org> 3.900.0-1mdv2010.1
+ Revision: 484437
- update to 3.9

* Thu Jul 23 2009 Jérôme Quelin <jquelin@mandriva.org> 3.700.0-1mdv2010.0
+ Revision: 398943
- update to 3.7

  + Götz Waschk <waschk@mandriva.org>
    - remove the macro definition again

* Fri May 08 2009 Götz Waschk <waschk@mandriva.org> 3.600.0-1mdv2010.0
+ Revision: 373389
- add perl_convert_version macro
- new version
- use perl version macro

* Thu Feb 19 2009 Götz Waschk <waschk@mandriva.org> 3.53-1mdv2009.1
+ Revision: 342889
- update to new version 3.53

* Fri Jan 16 2009 Götz Waschk <waschk@mandriva.org> 3.52-1mdv2009.1
+ Revision: 330121
- update to new version 3.52

* Fri Dec 05 2008 Götz Waschk <waschk@mandriva.org> 3.42-2mdv2009.1
+ Revision: 310611
- new version
- fix source URL

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 3.42-2mdv2009.0
+ Revision: 268457
- rebuild early 2009.0 package (before pixel changes)

* Wed May 28 2008 Götz Waschk <waschk@mandriva.org> 3.42-1mdv2009.0
+ Revision: 212537
- new version

* Mon Jan 21 2008 Götz Waschk <waschk@mandriva.org> 2.01-1mdv2008.1
+ Revision: 155533
- new version

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 1.3-2mdv2008.1
+ Revision: 151426
- rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 26 2007 Götz Waschk <waschk@mandriva.org> 1.3-1mdv2008.1
+ Revision: 112075
- import perl-EV


* Mon Nov 26 2007 Götz Waschk <waschk@mandriva.org> 1.3-1mdv2008.1
- initial package

