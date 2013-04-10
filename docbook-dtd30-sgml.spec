%define dtdver 3.0
%define mltyp sgml
%define sgmlbase %{_datadir}/sgml

Summary:	SGML document type definition for DocBook %{dtdver}
Name:		docbook-dtd30-sgml
Version:	1.0
Release:	13
Group:		Publishing
License:	Distributable
Url:		http://www.oasis-open.org/docbook/
# Zip file downloadable at http://www.oasis-open.org/docbook/sgml/%{dtdver}/
Source0:	docbk30.tar.bz2 
Patch0:		%{name}-%{version}.catalog.patch
BuildArch:	noarch  
Provides:	docbook-dtd-sgml
Requires:	sgml-common >= 0.6.3-2mdk

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is SGML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -q 
%apply_patches

%build

%install
DESTDIR=%{buildroot}%{sgmlbase}/docbook/sgml-dtd-%{dtdver}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
mkdir -p %{buildroot}%{_sysconfdir}/sgml
touch %{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
touch %{buildroot}%{_sysconfdir}/sgml/catalog

%files
%doc *.txt
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/catalog
%{sgmlbase}/docbook/sgml-dtd-%{dtdver}

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
 
