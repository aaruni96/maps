prefix = /usr/local
sysconfdir=/etc

all:
	echo "Python package doesn't need compiling!"

install:
	install src/maps $(DESTDIR)$(prefix)/bin/maps
	install --mode 644 src/completion.bash $(DESTDIR)$(prefix)/share/bash-completion/completions/maps
	install --mode 644 src/usr.bin.maps $(DESTDIR)$(sysconfdir)/apparmor.d/usr.bin.maps

clean:
	echo "nothing to compile, so nothing to clean!"
