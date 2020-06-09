# vim: et:ts=2:sw=2:sts=2

%global commit d0aa8060948d95c1575f39a471ab3b3c71572c03
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:       opencast-influxdb-adapter-legacy
Summary:    Stores statistical data, parsed from webserver logs, in InfluxDB
Version:    0
Release:    6.%{shortcommit}%{?dist}
License:    ECL 2.0
URL:        https://github.com/opencast/opencast-influxdb-adapter
Source0:    https://github.com/wsmirnow/opencast-influxdb-adapter/archive/%{commit}/opencast-influxdb-adapter-%{shortcommit}.tar.gz
Source1:    opencast-influxdb-adapter.logrotate
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root


%{?systemd_requires}
BuildRequires:  systemd
BuildRequires:  java-devel >= 1:1.8.0
BuildRequires:  maven >= 3.1
Requires:       java-headless >= 1:1.8.0


%description
Parses the webserver log file, extract and filter media file URLs,
enrich the data with series metadata from Opencast and write the data into an influx db.


%prep
%autosetup -n opencast-influxdb-adapter-%{commit}


%build
mvn clean install


%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d \
  %{buildroot}%{_sysconfdir}/%{name} \
  %{buildroot}%{_datadir}/%{name} \
  %{buildroot}%{_unitdir} \
  %{buildroot}%{_localstatedir}/log/%{name}
install -p -m 644 build/opencast-influxdb-adapter-2.0.jar %{buildroot}%{_datadir}/%{name}/%{name}-2.0.jar
install -p -m 644 docs/opencast-influxdb-adapter-logback.xml %{buildroot}%{_sysconfdir}/%{name}/%{name}-logback.xml
install -p -m 644 docs/opencast-influxdb-adapter.properties %{buildroot}%{_sysconfdir}/%{name}/%{name}.properties
install -p -m 644 docs/opencast-influxdb-adapter.service %{buildroot}%{_unitdir}/%{name}.service
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# patch log file configuration
sed -i 's#logback-sample\.xml#%{_sysconfdir}/%{name}/%{name}-logback.xml#' \
  %{buildroot}%{_sysconfdir}/%{name}/%{name}.properties

# patch log file location
sed -i 's#/var/log/opencast/influxdb-adapter\.log#%{_localstatedir}/log/%{name}/%{name}.log#' \
  %{buildroot}%{_sysconfdir}/%{name}/%{name}-logback.xml

# patch systemd service file
sed -i 's#/opt/opencast-influxdb-adapter#%{_datadir}/%{name}#' \
  %{buildroot}%{_unitdir}/%{name}.service
sed -i 's#opencast-influxdb-adapter-2\.0\.jar$#%{name}-2.0.jar --config-file=%{_sysconfdir}/%{name}/%{name}.properties#' \
  %{buildroot}%{_unitdir}/%{name}.service

# patch logrotate
sed -i 's#/var/log/opencast-influxdb-adapter#%{_localstatedir}/log/%{name}#' \
  %{buildroot}%{_sysconfdir}/logrotate.d/%{name}


%pre


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.service


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/%{name}-2.0.jar
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-logback.xml
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.properties
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%license LICENSE
%doc NOTICES
%doc README.md
%attr(-,root,root) %{_localstatedir}/log/%{name}


%changelog
* Tue Jun 09 2020 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-6
- based on opencast-influxdb-adapter
- parses legacy matterhon URLs
- service run as root user per default
- Version 0-5.d0aa806

* Wed Dec 04 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-5
- Version 0-5.ed44ce6

* Wed Oct 23 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-4
- Version 0-4.162dbea

* Wed Oct 23 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-3
- Version 0-3.64d5ae7

* Tue Oct 22 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-2
- Unit tests enabled

* Tue Oct 22 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-1
- Initial build
