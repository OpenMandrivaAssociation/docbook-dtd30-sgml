%define dtdver 3.0
%define mltyp sgml
%define sgmlbase %{_datadir}/sgml

%define name docbook-dtd30-sgml
%define version 1.0
%define release %mkrel 10

Name:			%{name}
Version:		%{version}
Release:		%{release}
Group:			Publishing

Summary: SGML document type definition for DocBook %{dtdver}

License:		Distributable
URL:			http://www.oasis-open.org/docbook/

Provides:		docbook-dtd-sgml
Requires:		sgml-common >= 0.6.3-2mdk

BuildRoot: %{_tmppath}/%{name}-buildroot

# Zip file downloadable at http://www.oasis-open.org/docbook/sgml/%{dtdver}/
Source0:		docbk30.tar.bz2 
Patch0:			%{name}-%{version}.catalog.patch
BuildArch: noarch  


%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is SGML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.


%prep
%setup -q 
%patch0 -p1 -b .catalog

%build


%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT%{sgmlbase}/docbook/sgml-dtd-%{dtdver}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (0644,root,root,0755)
%doc *.txt
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/catalog
%{sgmlbase}/docbook/sgml-dtd-%{dtdver}

# fix errors in old postun scripts
%triggerpostun -- docbook-dtd30-sgml < 1.0-3mdk
if [ -e %{_datadir}/sgml/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/openjade/catalog
fi
if [ -e %{_datadir}/sgml/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/docbook/dsssl-stylesheets/catalog
fi

%post
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{_datadir}/sgml/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{_datadir}/sgml/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{_datadir}/sgml/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/openjade/catalog
fi
if [ -e %{_datadir}/sgml/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/docbook/dsssl-stylesheets/catalog
fi


%postun
# Do not remove if upgrade
if [ "$1" = "0" -a -x %{_bindir}/xmlcatalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{_datadir}/sgml/docbook/%{mltyp}-dtd-%{dtdver}/catalog

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{_datadir}/sgml/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{_datadir}/sgml/openjade/catalog
  fi

  if [ -e %{_datadir}/sgml/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{_datadir}/sgml/docbook/dsssl-stylesheets/catalog
  fi
fi
 
