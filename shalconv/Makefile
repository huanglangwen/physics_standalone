SERBOX=/usr/local/serialbox

TARGET = main.x

SRC = \
  m_countdown.F \
  machine.F \
  physcons.F \
  funcphys.F \
  samfaerosols.F \
  samfshalcnv.F \
  main.F

OBJ = $(SRC:.F=.o)
PP = $(SRC:.F=.F90)

F90 = gfortran
FFLAGS = -fdec -fdefault-real-8 -fno-fast-math -ffree-form -ffree-line-length-none \
	-fno-backslash -fimplicit-none -frange-check -pedantic -Waliasing -Wampersand \
	-Wline-truncation -Wsurprising -Wtabs -Wunderflow -O0 -g -fbacktrace -fdump-core \
	-ffpe-trap=invalid,zero,overflow -fbounds-check -finit-real=nan -finit-integer=9999999 \
	-finit-logical=true -finit-character=35 -DSERIALIZE -I$(SERBOX)/include
LD = gfortran
LDFLAGS = $(SERBOX)/lib/libSerialboxFortran.a $(SERBOX)/lib/libSerialboxC.a $(SERBOX)/lib/libSerialboxCore.a -L/lib/x86_64-linux-gnu -lnetcdff -lnetcdf -lpthread -lstdc++ -lstdc++fs

.PHONY: all
all: pre-process $(TARGET)

.PHONY: pre-process
pre-process: $(PP)

.PHONY: clean
clean:
	/bin/rm -f *.mod *.o $(PP)

.PHONY: distclean
distclean: clean
	/bin/rm -rf $(TARGET) data data.tar.gz

$(TARGET): $(OBJ)
	$(LD) $(OBJ) $(LDFLAGS) -o $(TARGET)

%.F90: %.F
	$(SERBOX)/python/pp_ser/pp_ser.py --no-prefix -v --output=$@ $<

%.o: %.F90
	$(F90) $(FFLAGS) -c $< -o $@

