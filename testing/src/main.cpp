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

//sf::Color::Color(Uint8 red, Uint8 green, Uint8 blue, Uint8 alpha = 255) 	

std::vector<std::pair<Particle, sf::RectangleShape>> generateImage(int height, int width);
void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities);

int main() {
    srand(time(NULL));
    int height = 900;
    int width = 900;
    int i = 0;
    bool generated = false;
    sf::RenderWindow window(sf::VideoMode(height, width), "It works");
    sf::Vector2<int> placement;
    std::vector<std::pair<Particle, sf::RectangleShape>> pixels;
    std::cout << "Creating animation" << std::endl;
    while (window.isOpen()) {
        window.setFramerateLimit(0);
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear();
        if (!generated) {
            pixels = generateImage(height, width);
            generated = true;
        } else {
            move(pixels);
        }
        for (auto obj : pixels) {
            window.draw(obj.second);
        }

        window.display();
    }

    return 0;
}

std::vector<std::pair<Particle, sf::RectangleShape>> generateImage(int height, int width) {
    int amount = 250;
    int entity_size = 10;
    float posx = 0.f;
    float posy;
    int ax = 50;
    int ay = 50;
    int hx = 200;
    int hy = 100;
    std::vector<std::pair<Particle, sf::RectangleShape>> pixels;
    for (int i = 0; i < amount; i++) {
        Particle alliance(0, ax, ay, 5, 1);
        Particle horde(1, hx, hy, 5, 1);
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
    return pixels;
}

void move(std::vector<std::pair<Particle, sf::RectangleShape>> &entities) {
    std::vector<std::pair<Particle, sf::RectangleShape>> refresh;
    int times = 0;
    bool dead = false;
    for (auto enity : entities) {
        if (enity.first.getHealth() <= 0) {
            dead = true;
            std::cout << "DELETED" << std::endl;
        } else {
            sf::Vector2f curpos = enity.second.getPosition();
            int move = rand() % 4;
            switch(move) {
                case 0:
                    (0 <= curpos.y+1.f && curpos.y+1.f <= 900) ? enity.second.setPosition(curpos.x, curpos.y+1.f) : enity.second.setPosition(curpos.x, curpos.y);
                    break;
                case 1:
                    (0 <= curpos.x+1.f && curpos.x+1.f <= 900) ? enity.second.setPosition(curpos.x+1.f, curpos.y) : enity.second.setPosition(curpos.x, curpos.y);
                    break;
                case 2:
                    (0 <= curpos.y-1.f && curpos.y-1.f <= 900) ? enity.second.setPosition(curpos.x, curpos.y-1.f) : enity.second.setPosition(curpos.x, curpos.y);
                    break;
                case 3:
                    (0 <= curpos.x-1.f && curpos.x-1.f <= 900) ? enity.second.setPosition(curpos.x-1.f, curpos.y) : enity.second.setPosition(curpos.x, curpos.y);
                    break;
                default:
                    break;
            }
            // 
    //if (rect1.x < rect2.x + rect2.width &&
    //   rect1.x + rect1.width > rect2.x &&
    //   rect1.y < rect2.y + rect2.height &&
    //   rect1.y + rect1.height > rect2.y) {
        // collision detected!
    //}
            for (auto enemies : entities) {
                if (enemies.second.getPosition() != enity.second.getPosition()) {
                    if (enemies.second.getFillColor() != enity.second.getFillColor()) {
                        sf::Vector2f enemy_pos = enemies.second.getPosition();
                        if (enemy_pos.x < curpos.x + 10 && 
                            enemy_pos.x + 10 > curpos.x && 
                            enemy_pos.y < curpos.y + 10 &&
                            enemy_pos.y + 10 > curpos.y) {
                            std::cout << "COLLISION" << std::endl;
                            /*int dmgx = enemies.first.getHealth() - enity.first.getHealth();
                            int dmgy = enity.first.getHealth() - enemies.first.getStrength();
                            enemies.first.setHealth(dmgx);
                            enity.first.setHealth(dmgy);
                            if (enity.first.getHealth() <= 0)
                            {
                                dead = true;
                                std::cout << "DEAD" << std::endl;
                            }*/
                            dead = true;
                            break;
                        }
                    }
                }
            }
        }
        if (!dead)
            refresh.emplace_back(enity.first, enity.second);
    }
    entities = refresh;
}
