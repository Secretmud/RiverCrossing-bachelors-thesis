LIBS=-lsfml-graphics -lsfml-window -lsfml-system
CXX := g++

all: animation

%.o: %.cpp
        $(CXX) -c $< -o $@

%.o: %.hpp
        $(CXX) -c $< -o $@

animation: Game.o State.o PlayState.o Object.o Player.o
        @echo "** Building the game"
        $(CXX) -o animation Game.o State.o PlayState.o Object.o Player.o $(LIBS)

clean:
        @echo "** Removing object files and executable..."
        rm -f animation *.o

install:
        @echo '** Installing...'
        cp animation /usr/bin/

uninstall:
        @echo '** Uninstalling...'
        $(RM) /usr/bin/animation
