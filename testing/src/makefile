LIBS=-lsfml-graphics -lsfml-window -lsfml-system -fopenmp
CXX := g++

all: animation

%.o: %.cpp
	$(CXX) -c $< -o $@

%.o: %.hpp
	$(CXX) -c $< -o $@

animation: 
	@echo "** Building the game"
	$(CXX) -c main.cpp simulation/particle/*.hpp simulation/particle/*.cpp
	$(CXX) -o animation *.o $(LIBS)

clean: animation
	@echo "** Removing object files and executable..."
	rm -f animation *.o
