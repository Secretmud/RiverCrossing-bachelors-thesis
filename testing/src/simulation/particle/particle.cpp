#include "particle.hpp"
#include <vector>



Particle::Particle(int faction, int width, int height, int health, int strength)
    : faction(faction), width(width), height(height), health(health), strength(strength) {}

void Particle::setWidth(int width) {
    this->width = width;
}

void Particle::setHeight(int height) {
    this->height = height;
}

int Particle::getWidth() {
    return this->width;
}

int Particle::getHeight() {
    return this->height;
}

int Particle::getFaction() {
    return this->faction;
}

void Particle::setHealth(int attack) {
    this->health = this->health - attack;
}

int Particle::getHealth() {
    return this->health;
}

void Particle::setStrength(int strength) {
    this->strength = strength;
}

int Particle::getStrength() {
    return this->strength;
}


// Alliance blue: 32, 156, 201
// Horde red: 191, 42, 42

std::vector<int> Particle::getColor() {
    std::vector<int> alliance = {32, 156, 201, 255};
    std::vector<int> horde = {191, 42, 42, 255};
    return (this->faction == 0) ? alliance : horde;
}
