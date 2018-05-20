# config
SHELL = /bin/bash

# constants
EXCLUDE_FILE = deploy_excludes.txt
ROPTIONS     = --recursive --verbose --executability --times --perms --exclude-from $(EXCLUDE_FILE)

DEPLOY_DIR    = /home/dblotsky/Developer/html/stringfuzz_site
DEPLOY_USER   = dblotsky
DEPLOY_SERVER = dmitryblotsky.com

JEKYLL_ARGS = --source $(SRC_DIR) --destination $(BUILD_DIR) --config $(CONFIG)

# directories
SRC_DIR         = site
BUILD_DIR       = _build
PROBLEM_DIR     = problems
RESULTS_DIR     = ../runs
DATA_DIR        = $(SRC_DIR)/_data
STATIC_DIR      = $(SRC_DIR)/static
ZIP_DIR         = $(STATIC_DIR)/zip
SAMPLE_DIR      = $(STATIC_DIR)/txt/samples
RESULTS_LINK    = $(STATIC_DIR)/results
RESULT_PAGE_DIR = $(SRC_DIR)/_results

BENCH_DIR = $(STATIC_DIR)/csv/benchmarks
PLOT_DIR = $(STATIC_DIR)/svg/plots

# files
CONFIG = _config.yml

PROBLEMS_FILE     = $(DATA_DIR)/problems.yml
PROBLEMS_FILE_SRC = $(DATA_DIR)/problems-source.yml
HTML_SOURCES      = $(shell find $(SRC_DIR) -name *.html -or -name *.md)
JS_SOURCES        = $(shell find $(SRC_DIR) -name *.js)
CSS_SOURCES       = $(shell find $(SRC_DIR) -name *.css)
DATA_SOURCES      = $(shell find $(SRC_DIR) -name *.yml) $(PROBLEMS_FILE)
PROBLEM_ARCHIVE   = $(ZIP_DIR)/problems.zip

RESULT_NAMES = $(shell ls $(RESULTS_LINK))
RESULT_PAGES = $(addsuffix .md,$(addprefix $(RESULT_PAGE_DIR)/,$(RESULT_NAMES)))

SOURCES = $(HTML_SOURCES) $(JS_SOURCES) $(CSS_SOURCES) $(DATA_SOURCES) $(RESULT_PAGES)

# tools
FUZZER = stringfuzzg
JEKYLL = bundle exec jekyll

# convenience targets
default all: $(BUILD_DIR)

install: rbinstall pyinstall

rbinstall: vendor/bundle

pyinstall: requirements.txt
	pip install -r requirements.txt

build: $(BUILD_DIR)

serve: $(BUILD_DIR)
	$(JEKYLL) serve $(JEKYLL_ARGS)

bench: $(BENCH_DIR)

plot: $(PLOT_DIR)

zips: $(ZIP_DIR)

results: $(RESULT_PAGES)

link_results: $(RESULTS_LINK)

deploy: $(BUILD_DIR)
	rsync $(ROPTIONS) $(BUILD_DIR)/ $(DEPLOY_USER)@$(DEPLOY_SERVER):$(DEPLOY_DIR)/

# real targets
/usr/local/bin/bundle:
	gem install bundle

./vendor/bundle: Gemfile /usr/local/bin/bundle
	bundle

$(BENCH_DIR): $(PROBLEM_DIR)
	mkdir -p $(BENCH_DIR)
	python3 bin/bench.py $(PROBLEM_DIR) $(BENCH_DIR)

$(PLOT_DIR): $(BENCH_DIR)
	mkdir -p $(PLOT_DIR)
	python3 bin/plot.py $(BENCH_DIR) $(PLOT_DIR)

$(RESULTS_LINK): $(RESULTS_DIR)
	ln -s $(realpath $(RESULTS_DIR)) $(RESULTS_LINK)

$(BUILD_DIR): $(SOURCES) $(ZIP_DIR) $(PROBLEM_ARCHIVE) $(SAMPLE_DIR)
	$(JEKYLL) build $(JEKYLL_ARGS)

$(PROBLEMS_FILE): $(PROBLEMS_FILE_SRC) bin/render_problem_list.py
	python3 bin/render_problem_list.py $< < $< > $@

$(PROBLEM_DIR): $(PROBLEMS_FILE) bin/make_problems.py
	python3 bin/make_problems.py $@ $(PROBLEMS_FILE)
	touch $(PROBLEM_DIR)

$(ZIP_DIR): $(PROBLEM_DIR)
	mkdir -p $@
	for suite_name in `ls $(PROBLEM_DIR)`; do \
		pushd $(PROBLEM_DIR) && zip -r $$suite_name $$suite_name && popd; \
		mv $(PROBLEM_DIR)/$$suite_name.zip $@; \
	done

$(PROBLEM_ARCHIVE): $(ZIP_DIR) $(PROBLEM_DIR)
	zip -r $(PROBLEM_DIR) problems
	mv problems.zip $(ZIP_DIR)

$(SAMPLE_DIR): $(PROBLEM_DIR)
	mkdir -p $@
	for suite in `ls $(PROBLEM_DIR)`; do \
		ls $(PROBLEM_DIR)/$$suite/*.smt20 | grep -v "\-model" | head -n 1 | xargs -I% cp % $(SAMPLE_DIR)/$$suite-first.smt20.txt; \
		ls $(PROBLEM_DIR)/$$suite/*.smt20 | grep -v "\-model" | tail -n 1 | xargs -I% cp % $(SAMPLE_DIR)/$$suite-last.smt20.txt; \
		ls $(PROBLEM_DIR)/$$suite/*.smt25 | grep -v "\-model" | head -n 1 | xargs -I% cp % $(SAMPLE_DIR)/$$suite-first.smt25.txt; \
		ls $(PROBLEM_DIR)/$$suite/*.smt25 | grep -v "\-model" | tail -n 1 | xargs -I% cp % $(SAMPLE_DIR)/$$suite-last.smt25.txt; \
	done
	touch $(SAMPLE_DIR)

$(SRC_DIR)/_results/%.md: $(RESULTS_LINK)/% bin/make_date.py | $(RESULTS_LINK)
	echo '---' > $@
	python3 bin/make_date.py $@ >> $@
	echo '---' >> $@
	echo '' >> $@

# maintenance
clean:
	$(RM) $(PROBLEMS_FILE)
	$(RM) -r $(BUILD_DIR)
	$(RM) -r .sass-cache
	$(RM) $(PROBLEM_ARCHIVE)
	bundle clean

nuke: clean
	$(RM) $(RESULT_PAGE_DIR)/*.md
	$(RM) -r $(PROBLEM_DIR)
	$(RM) -r $(ZIP_DIR)
