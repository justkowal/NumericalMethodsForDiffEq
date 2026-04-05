CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2 -fPIC -Iinclude
CFLAGS_DEBUG ?= -Wall -Wextra -g -O0 -Iinclude

SRCDIR = src
INCDIR = include
OBJDIR = obj
LIBDIR = lib
EXDIR = examples
BINDIR = bin

SOURCES = $(wildcard $(SRCDIR)/*.c)
HEADERS = $(wildcard $(INCDIR)/*.h)
OBJECTS = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SOURCES))

LIB_NAME = $(LIBDIR)/libode_solver.a
LIB_SHARED = $(LIBDIR)/libode_solver.so

EXAMPLES_SRC = $(EXDIR)/rocket_complex.c
EXAMPLES_BIN = $(patsubst $(EXDIR)/%.c, $(BINDIR)/%, $(EXAMPLES_SRC))

all: dirs $(LIB_NAME) $(EXAMPLES_BIN)

dirs:
	@mkdir -p $(OBJDIR) $(LIBDIR) $(BINDIR)

$(LIB_NAME): $(OBJECTS)
	@mkdir -p $(LIBDIR)
	ar rcs $@ $^
	@echo "✓ Static library built: $@"

$(LIB_SHARED): $(OBJECTS)
	@mkdir -p $(LIBDIR)
	$(CC) -shared -o $@ $^
	@echo "✓ Shared library built: $@"

$(OBJDIR)/%.o: $(SRCDIR)/%.c $(HEADERS)
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c -o $@ $<

$(BINDIR)/%: $(EXDIR)/%.c $(LIB_NAME)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS) -o $@ $< -L$(LIBDIR) -lode_solver -lm
	@echo "✓ Example built: $@"

debug: CFLAGS = $(CFLAGS_DEBUG)
debug: clean all
	@echo "✓ Debug build complete"

shared: dirs $(LIB_SHARED)

clean:
	rm -rf $(OBJDIR) $(LIBDIR) $(BINDIR)
	@echo "✓ Cleaned"

install: $(LIB_NAME) $(HEADERS)
	install -d /usr/local/lib
	install -d /usr/local/include
	install $(LIB_NAME) /usr/local/lib/
	install $(HEADERS) /usr/local/include/
	@echo "✓ Installed to /usr/local"

info:
	@echo "ODE Solver Library Makefile"
	@echo "Targets:"
	@echo "  all          - Build static library and examples (default)"
	@echo "  shared       - Build shared library"
	@echo "  debug        - Build with debug symbols"
	@echo "  clean        - Remove built directories"
	@echo "  install      - Install to /usr/local"
	@echo "  info         - Show this message"

.PHONY: all shared debug clean install info dirs
