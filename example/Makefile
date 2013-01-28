BOOTSTRAP_LESS = ./web/less/bootstrap/bootstrap.less
BOOTSTRAP_RESPONSIVE_LESS = ./web/less/bootstrap/responsive.less

static:
	lessc -x web/less/style.less > web/css/style.css
	cat web/js/libs/bootstrap/bootstrap-transition.js \
		web/js/libs/bootstrap/bootstrap-alert.js \
		web/js/libs/bootstrap/bootstrap-button.js \
		web/js/libs/bootstrap/bootstrap-carousel.js \
		web/js/libs/bootstrap/bootstrap-collapse.js \
		web/js/libs/bootstrap/bootstrap-dropdown.js \
		web/js/libs/bootstrap/bootstrap-modal.js \
		web/js/libs/bootstrap/bootstrap-tooltip.js \
		web/js/libs/bootstrap/bootstrap-popover.js \
		web/js/libs/bootstrap/bootstrap-scrollspy.js \
		web/js/libs/bootstrap/bootstrap-tab.js \
		web/js/libs/bootstrap/bootstrap-typeahead.js \
		web/js/libs/bootstrap/bootstrap-affix.js > web/js/libs/bootstrap.js
	python manage.py collectstatic --noinput --ignore "*.less" --ignore "bootstrap"

clean:
	rm -rf public/static*
	rm web/css/style.css

bootstrap:
	mkdir -p web/css/bootstrap
	mkdir -p web/js/bootstrap
	recess --compile ${BOOTSTRAP_LESS} > web/css/bootstrap/bootstrap.css
	recess --compress ${BOOTSTRAP_LESS} > web/css/bootstrap/bootstrap.min.css
	recess --compile ${BOOTSTRAP_RESPONSIVE_LESS} > web/css/bootstrap/bootstrap-responsive.css
	recess --compress ${BOOTSTRAP_RESPONSIVE_LESS} > web/css/bootstrap/bootstrap-responsive.min.css
	cat web/js/libs/bootstrap/bootstrap-transition.js web/js/libs/bootstrap/bootstrap-alert.js web/js/libs/bootstrap/bootstrap-button.js web/js/libs/bootstrap/bootstrap-carousel.js web/js/libs/bootstrap-collapse.js web/js/libs/bootstrap/bootstrap-dropdown.js web/js/libs/bootstrap/bootstrap-modal.js web/js/libs/bootstrap/bootstrap-tooltip.js web/js/libs/bootstrap/bootstrap-popover.js web/js/libs/bootstrap/bootstrap-scrollspy.js web/js/libs/bootstrap/bootstrap-tab.js web/js/libs/bootstrap/bootstrap-typeahead.js web/js/libs/bootstrap/bootstrap-affix.js > web/js/libs/bootstrap/bootstrap.js
	uglifyjs -nc web/js/libs/bootstrap/bootstrap.js > web/js/libs/bootstrap/bootstrap.min.tmp.js
	echo "/*!\n* Bootstrap.js by @fat & @mdo\n* Copyright 2012 Twitter, Inc.\n* http://www.apache.org/licenses/LICENSE-2.0.txt\n*/" > web/js/libs/bootstrap/copyright.js
	cat web/js/libs/bootstrap/copyright.js web/js/libs/bootstrap/js/bootstrap.min.tmp.js > web/js/libs/bootstrap/bootstrap.min.js
	rm web/js/libs/bootstrap/copyright.js web/js/libs/bootstrap/bootstrap.min.tmp.js

.PHONY : clean
.PHONY : static
