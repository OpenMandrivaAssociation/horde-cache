%define prj    Horde_Cache

%define xmldir  %{_var}/lib/pear
%define peardir %(pear config-get php_dir 2> /dev/null)

Name:          horde-cache
Version:       0.0.2
Release:       %mkrel 2
Summary:       Caching API
License:       LGPL
Group:         Networking/Mail
Url:           http://pear.horde.org/index.php?package=%{prj}
Source0:       %{prj}-%{version}.tgz
BuildArch:     noarch
Requires(pre): php-pear
Requires:      php-pear
Requires:      horde-util
BuildRequires: php-pear
BuildRequires: php-pear-channel-horde

%description
This package provides a simple, functional Caching API, with the option
to store the cached data either on the filesystem, or using the Zend
Performance Suite's content cache.


%prep
%setup -q -n %{prj}-%{version}

%build
%__mv ../package.xml .

%install
pear install --packagingroot %{buildroot} --nodeps package.xml

%__rm -rf %{buildroot}/%{peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

%__mkdir_p %{buildroot}%{xmldir}
%__cp package.xml %{buildroot}%{xmldir}/%{prj}.xml

%clean
%__rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/%{prj}.xml

%postun
if [ "$1" -eq "0" ]; then
  pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/%{prj}
fi

%files
%defattr(-, root, root)
%{xmldir}/%{prj}.xml
%dir %{peardir}/Horde/Cache
%{peardir}/Horde/Cache.php
%{peardir}/Horde/Cache/file.php
%{peardir}/Horde/Cache/memcache.php
%{peardir}/Horde/Cache/zps4.php

