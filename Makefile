CXX = g++
CXXFLAGS = -Wall -fPIC -O3 -msse2
ifeq ($(no_omp), 1)
	CXXFLAGS += -DDISABLE_OPENMP
else
	CXXFLAGS += -fopenmp
endif

LDFLAGS =

DIR_SRC = src
DIR_BUILD = build
DIR_LIB = lib
SRC = $(wildcard $(DIR_SRC)/*.cpp $(DIR_SRC)/*/*.cpp)
OBJ = $(patsubst $(DIR_SRC)%.cpp, $(DIR_BUILD)%.o, $(SRC))

LOTER_DYLIB = libloter.so

.PHONY: clean Rpack Rbuild Rcheck

all: $(DIR_LIB)/$(LOTER_DYLIB)

$(DIR_LIB)/$(LOTER_DYLIB): $(OBJ)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

$(DIR_BUILD)/%.o: $(DIR_SRC)/%.cpp
	@mkdir -p $(@D)
	$(CXX) -c $(CXXFLAGS) $< -o $@

clean:
	rm -rf lib build loter R-package/src/src_libloter

cleanR:
	rm -rf loter.Rcheck
	rm -f loter*.tar.gz

cleanall: clean cleanR

Rpack:
	$(MAKE) clean
	rm -rf R-package/src/src_libloter
	rm -f R-package/src/loter.so
	mkdir R-package/src/src_libloter
	cp -R src/* R-package/src/src_libloter
	mkdir loter
	cp -R R-package/* loter

Rbuild:
	$(MAKE) Rpack
	R CMD build --no-build-vignettes loter
	rm -rf loter

Rcheck:
	$(MAKE) Rbuild
	R CMD check loter*.tar.gz
