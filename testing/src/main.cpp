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

void generateImage(int height, int width, std::vector<std::pair<Particle, sf::RectangleShape>> &pixels);
void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities);
void newParticle(Particle &p, int faction, sf::RectangleShape &rec);

int main() {
    srand(time(NULL));
    int height = 900;
    int width = 900;
    sf::RenderWindow window(sf::VideoMode(height, width), "It works");
    sf::Vector2<int> placement;
    std::vector<std::pair<Particle, sf::RectangleShape>> pixels;
    generateImage(height, width, pixels);
    std::cout << "Creating animation" << std::endl;
    while (window.isOpen()) {
        window.setFramerateLimit(0);
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear();
        move(pixels);
        for (auto obj : pixels) {
            window.draw(obj.second);
        }

        window.display();
    }

    return 0;
}

void generateImage(int height, int width, std::vector<std::pair<Particle, sf::RectangleShape>> &pixels) {
    int amount = 250;
    int entity_size = 10;
    float posx = 0.f;
    float posy;
    int ax = 50;
    int ay = 50;
    int hx = 150;
    int hy = 150;
    for (int i = 0; i < amount; i++) {
        Particle alliance(0, ax, ay, 1, 1, i);
        Particle horde(1, hx, hy, 1, 1, i+amount);
        sf::RectangleShape tmp1(sf::Vector2f(entity_size, entity_size));
        sf::RectangleShape tmp2(sf::Vector2f(entity_size, entity_size));
        std::vector<int> x = alliance.getColor();
        std::vector<int> y = horde.getColor();
        tmp1.setFillColor(sf::Color(x[0], x[1], x[2], x[3]));
        tmp2.setFillColor(sf::Color(y[0], y[1], y[2], y[3]));
        tmp1.setPosition(alliance.getWidth(), alliance.getHeight());
        tmp2.setPosition(horde.getWidth(), horde.getHeight());
        pixels.emplace_back(alliance, tmp1);
        pixels.emplace_back(horde, tmp2);
    }
}

void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities) {
    std::vector<std::pair<Particle, sf::RectangleShape>> refresh;
    int times = 0;
    for (auto entity : entities) {
        bool dead = false;
        if (entity.first.getHealth() <= 0) {
            std::cout << "DELETED" << std::endl;
            dead = true;
            break;
        } else {
            sf::Vector2f curpos = entity.second.getPosition();
            int rmove = rand() % 4;
            float move = 5.f;
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
                                enemies.first.setHealth(enemies.first.getHealth() - entity.first.getStrength());
                                entity.first.setHealth(entity.first.getHealth() - enemies.first.getStrength());
                                if (entity.first.getHealth() <= 0) {
                                    dead = true;
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            if (!dead) 
                refresh.emplace_back(entity.first, entity.second);
        }
        int i = 0;
        for (auto entity : refresh) {
                    std::cout << "NEW" << i << "\r";
            if (entity.first.getFaction() == 0) {
                    std::cout << "NEW" << i << "\r";
                if (entity.first.getHealth() >= 8) {
                    std::cout << "NEW" << i << "\r";
                    sf::RectangleShape rec(sf::Vector2f(10, 10));
                    Particle p(0, entity.first.getWidth(), entity.first.getHeight(), 5, 1, i);
                    newParticle(p, 0, rec);
                    refresh.emplace_back(p, rec);
                    std::cout << "NEW" << i << "\r";
                } else {
                    entity.first.setHealth(entity.first.getHealth() + 1);
                }
            }
            i++;
        }
        entities = refresh;
}

void newParticle(Particle &p, int faction, sf::RectangleShape &rec) {
    std::vector<int> x = p.getColor();
    rec.setFillColor(sf::Color(x[0], x[1], x[2], x[3]));
    rec.setPosition(p.getWidth(), p.getHeight());
}

