#include <vector>
#ifndef particle
#define particle

class Particle {
    public:
        Particle(int faction, int width, int height, int health, int strength);
        std::vector<int> getColor();
        // Getters
        int getHeight();
        int getWidth();
        int getHealth();
        int getStrength();
        int getFaction();
        // Setters
        void setHeight(int height);
        void setWidth(int width);
        void setHealth(int attack);
        void setStrength(int strength);
    private:
        int height;
        int width;
        int faction;
        int health;
        int strength;
};
#endif
