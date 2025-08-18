prefix = /usr/local
sysconfdir=/etc

all:
	echo "Python package doesn't need compiling!"

install:
	install src/maps $(DESTDIR)$(prefix)/bin/maps
	install --mode 644 src/completion.bash $(DESTDIR)$(prefix)/share/bash-completion/completions/maps
	if [$(apparmor_parser --version | head -n1 | awk '{print $4}' | cut -c1) -lt 4]; then\
		install --mode 644 src/maps-aa-profile-abi-3 $(DESTDIR)$(sysconfdir)/apparmor.d/usr.bin.maps;\
	else\
		install --mode 644 src/maps-aa-profile-abi-4 $(DESTDIR)$(sysconfdir)/apparmor.d/usr.bin.maps;\
	fi
	install --mode 644 src/maps.desktop $(DESTDIR)${prefix}/share/applications/maps.desktop
	xdg-mime default maps.desktop x-scheme-handler/maps
clean:
	echo "nothing to compile, so nothing to clean!"
