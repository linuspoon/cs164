.PHONY: clean really-clean default

CXX = c++

CXXFLAGS = -g

JAVAFLAGS = -g

LOADLIBS = 

default: 6 P7.class

6: 6-parser.o
	$(CXX) $(CXXFLAGS) -o $@ $< $(LOADLIBS)

6-parser.o: 6-parser.cc 6-lexer.cc

6-parser.cc : 6.y
	bison -o $@ --debug $<

6-lexer.cc: 6.l
	flex -o $@ $<

P7.class: P7.java
	javac $(JAVAFLAGS)  $<

clean:
	$(RM) *.o *.class *~ 
	$(RM) 6  6-*

really-clean: clean

