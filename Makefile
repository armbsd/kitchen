PROG=			kitchen
SRCS= 			kitchen.py
MAINTAINER=		eleutherius69@gmail.com
WWW=			https://github.com/armbsd/kitchen
LICENSE=		MIT
LICENSE_FILE=	${WRKSRC}/COPYING
USES=			python pip
SRCS= 			kitchen.py

install:
	@echo == install "${PROG}" ==
	@pip install .

clean:
	@echo == Clean "${PROG}" system files ==
	@rm -rf __pycache__ build ${PROG}.egg-info src/libs/__pycache__

remove:
	@echo == Remove "${PROG}" from your system ==
	@pip uninstall "${PROG}"
