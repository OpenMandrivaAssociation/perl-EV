%define pkgname EV
%define filelist %{pkgname}-%{version}-filelist
%define maketest 1
%define ver 3.6
%define perl_convert_version() %(perl -Mversion -le '$v=version->new(%{1})->normal; $v=~s/^v//; print $v')

Name:      perl-%pkgname
Summary:   Wrapper for the libev high-performance event loop library
Version:   %perl_convert_version %ver
Release:   %mkrel 1
License:   Artistic
Group:     Development/Perl
URL:       http://software.schmorp.de/pkg/EV.html
SOURCE:    http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/EV-%ver.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
BuildRequires: perl-devel
BuildRequires: perl-AnyEvent >= 1:2.6

%description
A thin wrapper around libev, a high-performance event loop. Intended
as a faster and less buggy replacement for the Event perl
module. Efficiently supports very high number of timers, scalable
operating system APIs such as epoll, kqueue and solaris's ports,
child/pid watchers and more.

%prep
%setup -q -n %{pkgname}-%{ver} 
chmod -R u+w %{_builddir}/%{pkgname}-%{ver}

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

