# vim: et:ts=2:sw=2:sts=2

%global commit 8208661fe01713db6043847953d69d7e35d770ee
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:      opencast-influxdb-adapter
Summary:   Stores statistical data, parsed from webserver logs, in InfluxDB
Version:   0
Release:   1.%{shortcommit}%{?dist}
License:   ECLv2
URL:       https://github.com/opencast/opencast-influxdb-adapter
Source0:   https://github.com/opencast/opencast-influxdb-adapter/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%{?systemd_requires}
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
BuildRequires: java-devel >= 1:1.8.0
BuildRequires: maven >= 3.1
Requires: java >= 1:1.8.0


%description
Parses the webserver log file, extract and filter media file URLs,
enrich the data with series metadata from Opencast and write the data into an influx db.


%prep
%autosetup -n %{name}-%{commit}


%build
mvn clean install -D skipTests


%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d \
  %{buildroot}%{_sysconfdir}/%{name} \
  %{buildroot}%{_datadir} \
  %{buildroot}%{_unitdir}
install -p -m 755 %{name}-2.0.jar %{buildroot}%{_datadir}
install -p -m 644 docs/%{name}-logback.xml %{buildroot}%{_sysconfdir}/%{name}
install -p -m 644 docs/%{name}.properties %{buildroot}%{_sysconfdir}/%{name}
install -p -m 644 %{name}.service %{buildroot}%{_unitdir}


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
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name} %{name}-logback.xml %{name}.properties

%changelog
* Mon Oct 22 2019 Waldemar Smirnow <waldemar.smirnow@gmail.com> - 0-1
- Initial build
