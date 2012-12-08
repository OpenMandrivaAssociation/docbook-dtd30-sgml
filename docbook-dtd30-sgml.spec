%define dtdver 3.0
%define mltyp sgml
%define sgmlbase %{_datadir}/sgml

%define name docbook-dtd30-sgml
%define version 1.0
%define release %mkrel 13

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
 


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-12mdv2011.0
+ Revision: 663794
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2011.0
+ Revision: 604799
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2010.1
+ Revision: 520684
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2010.0
+ Revision: 413362
- rebuild

* Sat Mar 21 2009 Funda Wang <fwang@mandriva.org> 1.0-8mdv2009.1
+ Revision: 359885
- fix patchnum

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-8mdv2009.0
+ Revision: 220668
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0-7mdv2008.1
+ Revision: 149186
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-6mdv2008.0
+ Revision: 18830
- clean spec; rebuild for new era


* Tue Jan 10 2006 Frederic Crozat <fcrozat@mandriva.com> 1.0-5mdk
- Rebuild

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-4mdk
- Fix uninstall when xmlcatalog is no longer present

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-3mdk
- Mark some files has ghost configuration files
- Fix typo in script
- Fix upgrade script

* Thu Jul 17 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-2mdk
- Rebuild and use more macros

