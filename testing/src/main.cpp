#include <SFML/Graphics.hpp>
#include "simulation/particle/particle.hpp"
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iostream>
#include <thread>         // std::this_thread::sleep_for
#include <chrono>         // std::chrono::seconds
#include <utility>
#include <algorithm>
#include <omp.h>

void generateImage(int height, int width, std::vector<std::pair<Particle, sf::RectangleShape>> &pixels);
void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities, int &c);
void newParticle(Particle &p, int faction, sf::RectangleShape &rec);
bool placement(std::vector<std::pair<Particle, sf::RectangleShape>> &entities, float pos[2]);
void find(Particle &p, sf::RectangleShape &rec);

int main() {
    srand(time(NULL));
    int height = 900;
    int width = 900;
    sf::RenderWindow window(sf::VideoMode(height, width), "It works");
    sf::Vector2<int> placement;
    std::vector<std::pair<Particle, sf::RectangleShape>> pixels;
    generateImage(height, width, pixels);
    std::cout << "Creating animation" << std::endl;
    bool paused = true;
    int c = 0;
    while (window.isOpen()) {
        window.setFramerateLimit(60);
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) {
            paused = (paused) ? false : true;
            std::cout << paused << std::endl;
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::R)) {
            generateImage(height, width, pixels);
        }
        if (!paused) {
            window.clear();
            move(pixels, c);
            #pragma omp parallel for
            for (auto obj : pixels) {
                window.draw(obj.second);
            }
        }
        c++;
        window.display();
    }

    return 0;
}

void generateImage(int height, int width, std::vector<std::pair<Particle, sf::RectangleShape>> &pixels) {
    pixels.clear();
    int amount = 50;
    int entity_size = 10;
    float posx = 0.f;
    float posy;
    int i = 0;
    while (i < amount){
        float apos[2] = {rand() % height,rand() % width};
        float hpos[2] = {rand() % height,rand() % width};
        if (placement(pixels, apos) && placement(pixels, hpos)) {
            Particle alliance(0, apos[0], apos[1], 5, 1, i);
            Particle horde(1, hpos[0], hpos[1], 10, 1, i+amount);
            sf::RectangleShape tmp1(sf::Vector2f(entity_size, entity_size));
            sf::RectangleShape tmp2(sf::Vector2f(entity_size, entity_size));
            newParticle(alliance, 0, tmp1);
            newParticle(horde, 0, tmp2);
            pixels.emplace_back(alliance, tmp1);
            pixels.emplace_back(horde, tmp2);
            i++;
        }
    }
}

void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities, int &c) {
    std::vector<std::pair<Particle, sf::RectangleShape>> refresh;
    for (auto entity : entities) {
        bool dead = false;
        sf::Vector2f curpos = entity.second.getPosition();
        int rmove = rand() % 4;
        float move = 10.f;
        switch(rmove) {
            case 0:
                (0 <= curpos.y+move && curpos.y+move <= 900) ? entity.second.setPosition(curpos.x, curpos.y+move) : entity.second.setPosition(curpos.x, curpos.y);
                break;
            case 1:
                (0 <= curpos.x+move && curpos.x+move <= 900) ? entity.second.setPosition(curpos.x+move, curpos.y) : entity.second.setPosition(curpos.x, curpos.y);
                break;
            case 2:
                (0 <= curpos.y-move && curpos.y-move <= 900) ? entity.second.setPosition(curpos.x, curpos.y-move) : entity.second.setPosition(curpos.x, curpos.y);
                break;
            case 3:
                (0 <= curpos.x-move && curpos.x-move <= 900) ? entity.second.setPosition(curpos.x-move, curpos.y) : entity.second.setPosition(curpos.x, curpos.y);
                break;
            default:
                    break;
        }
        for (auto enemies : entities) {
            if (enemies.second.getPosition() != entity.second.getPosition()) {
                if (enemies.second.getFillColor() != entity.second.getFillColor()) {
                    sf::Vector2f enemy_pos = enemies.second.getPosition();
                    if (enemy_pos.x < curpos.x + 10 && 
                        enemy_pos.x + 10 > curpos.x && 
                        enemy_pos.y < curpos.y + 10 &&
                        enemy_pos.y + 10 > curpos.y) {
                        enemies.first.setHealth(enemies.first.getHealth() + entity.first.getStrength());
                        entity.first.setHealth(5);
                        entity.first.setFaction(1);
                        std::vector<int> x = entity.first.getColor();
                        entity.second.setFillColor(sf::Color(x[0], x[1], x[2], x[3]));
                    }
                }
            }
        }
        if (entity.first.getFaction() == 0) {
            if (entity.first.getHealth() >= 20) {
                sf::RectangleShape rec(sf::Vector2f(10, 10));
                Particle p(0, entity.first.getWidth(), entity.first.getHeight(), 5, 1, 1);
                newParticle(p, 0, rec);
                refresh.emplace_back(p, rec);
                entity.first.setHealth(5);
                int die = rand() % 100;
                if (die >= 85) dead = true;
            } else {
                entity.first.setHealth(entity.first.getHealth() + 1);
            }
        } 
        
        if (entity.first.getFaction() == 1) {
            if (entity.first.getHealth() <= 0)
                dead = true;
            else
                entity.first.setHealth(entity.first.getHealth() - ((c % 5 == 0) ? 1 : 0));

        }

        if (!dead) 
            refresh.emplace_back(entity.first, entity.second);
    }
    entities = refresh;
    refresh.clear();
}

void newParticle(Particle &p, int faction, sf::RectangleShape &rec) {
    std::vector<int> x = p.getColor();
    rec.setFillColor(sf::Color(x[0], x[1], x[2], x[3]));
    rec.setPosition(p.getWidth(), p.getHeight());
}

bool placement(std::vector<std::pair<Particle, sf::RectangleShape>> &entities, float pos[2]) {
    for (auto entity : entities) {
        if (entity.second.getPosition() == sf::Vector2f(pos[0], pos[1])) return false;
    }
    return true;
}
