%define module EV

Summary:	Wrapper for the libev high-performance event loop library
Name:		perl-%{module}
Version:	4.33
Release:	1
License: 	Artistic
Group:		Development/Perl
Url:		https://metacpan.org/pod/EV
Source0:	http://www.cpan.org/modules/by-module/EV/EV-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildRequires:	perl-devel
BuildRequires:	perl-AnyEvent >= 1:2.6
BuildRequires:	perl(common::sense)
# for test
BuildRequires:	perl(Canary::Stability)

%description
A thin wrapper around libev, a high-performance event loop. Intended
as a faster and less buggy replacement for the Event perl
module. Efficiently supports very high number of timers, scalable
operating system APIs such as epoll, kqueue and solaris's ports,
child/pid watchers and more.

%files
%doc README Changes
%{perl_vendorarch}/EV.pm
%{perl_vendorarch}/EV
%{perl_vendorarch}/auto/EV
%{_mandir}/man3/EV*

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{module}-%{version}
#chmod -R u+w %{_builddir}/%{module}-%{version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="%{optflags}"
echo | %{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%make_build

%check
%make test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%make_install `perl -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

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

