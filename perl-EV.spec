%define upstream_name    EV
%define upstream_version 4.27

%define filelist %{upstream_name}-%{upstream_version}-filelist
%define maketest 1

Name:      perl-%{upstream_name}
Version:   %perl_convert_version %{upstream_version}
Release:	1

Summary:   Wrapper for the libev high-performance event loop library

License:   Artistic
Group:     Development/Perl
Url:       https://metacpan.org/pod/EV
Source0:   https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/%{upstream_name}-%{upstream_version}.tar.gz
Source100: %{name}.rpmlintrc

BuildRequires: perl-devel
BuildRequires: perl-AnyEvent >= 1:2.6
BuildRequires: perl(common::sense)
# for test
BuildRequires: perl(Canary::Stability)

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
CFLAGS="%{optflags}"
echo | %{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%make 

%check
%make test

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
%doc README Changes
%{perl_vendorarch}/EV.pm
%{perl_vendorarch}/EV
%{perl_vendorarch}/auto/EV
%{_mandir}/man3/EV*
