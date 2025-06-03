# import sys
# import random
# import math
# from PyQt6.QtWidgets import QApplication, QWidget
# from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPolygon, QBrush, QPainterPath, QRadialGradient, QLinearGradient
# from PyQt6.QtCore import QPoint, Qt, QTimer, QCoreApplication, QRectF
# import os
# import logging
# from heapq import heappush, heappop
#
# # Настройка логирования
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
#     os.path.dirname(QCoreApplication.applicationFilePath()),
#     'Qt', 'plugins'
# )
#
# class GameConfig:
#     CELL_SIZE = 20
#     MAP_WIDTH = 28
#     MAP_HEIGHT = 31
#     FPS = 60
#     GHOST_SPEED = 0.15
#     PACMAN_SPEED = 0.18
#     MODE_DURATIONS = {
#         'scatter': 7,
#         'chase': 20,
#         'frightened': 10
#     }
#     TOTAL_PELLETS = 244
#
# # Карта игры
# MAP_DATA = [
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
#     [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
#     [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,1,2,1,1,1,1,1,2,0,0,2,1,1,1,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,0,2,0,0,0,1,0,2,0,0,2,0,1,0,0,0,2,0,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
#     [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
#     [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
#     [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
#     [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# ]
#
# DIRECTIONS = {
#     'up': (0, -1),
#     'down': (0, 1),
#     'left': (-1, 0),
#     'right': (1, 0)
# }
#
# class Star:
#     def __init__(self, x, y, brightness, speed, size):
#         self.x = x
#         self.y = y
#         self.brightness = brightness
#         self.speed = speed
#         self.size = size
#
#     def update(self):
#         self.brightness += self.speed
#         if self.brightness > 255:
#             self.brightness = 255
#             self.speed = -self.speed
#         elif self.brightness < 50:
#             self.brightness = 50
#             self.speed = -self.speed
#
# class Ghost:
#     def __init__(self, x, y, color, name):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.name = name
#         self.behavior = 'chase'
#         self.direction = 'right'
#         self.frightened_timer = 0
#         self.home_x = x
#         self.home_y = y
#         self.speed = GameConfig.GHOST_SPEED
#         self.scatter_targets = {
#             'Blinky': (26, 1),
#             'Pinky': (1, 1),
#             'Inky': (26, 29),
#         }
#         self.target = self.scatter_targets[name]
#         self.path = []
#
#     def can_move_to(self, x, y):
#         grid_x = int(round(x))
#         grid_y = int(round(y))
#         if not (0 <= grid_x < GameConfig.MAP_WIDTH and 0 <= grid_y < GameConfig.MAP_HEIGHT):
#             return False
#         return MAP_DATA[grid_y][grid_x] != 1
#
#     def get_available_directions(self):
#         available = []
#         for direction, (dx, dy) in DIRECTIONS.items():
#             new_x = self.x + dx
#             new_y = self.y + dy
#             if self.can_move_to(new_x, new_y):
#                 available.append(direction)
#         return available
#
#     def get_opposite_direction(self, direction):
#         opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
#         return opposites.get(direction, direction)
#
#     def a_star(self, start_x, start_y, target_x, target_y):
#         start_x, start_y = int(round(start_x)), int(round(start_y))
#         target_x, target_y = int(round(target_x)), int(round(target_y))
#         open_set = [(0, start_x, start_y, [])]
#         closed_set = set()
#         g_score = {(start_x, start_y): 0}
#         f_score = {(start_x, start_y): abs(target_x - start_x) + abs(target_y - start_y)}
#
#         while open_set:
#             _, x, y, path = heappop(open_set)
#             if (x, y) == (target_x, target_y):
#                 return path
#             if (x, y) in closed_set:
#                 continue
#             closed_set.add((x, y))
#             for direction, (dx, dy) in DIRECTIONS.items():
#                 next_x, next_y = x + dx, y + dy
#                 if not self.can_move_to(next_x, next_y):
#                     continue
#                 tentative_g_score = g_score[(x, y)] + 1
#                 if (next_x, next_y) not in g_score or tentative_g_score < g_score[(next_x, next_y)]:
#                     g_score[(next_x, next_y)] = tentative_g_score
#                     f_score[(next_x, next_y)] = tentative_g_score + abs(target_x - next_x) + abs(target_y - next_y)
#                     new_path = path + [direction]
#                     heappush(open_set, (f_score[(next_x, next_y)], next_x, next_y, new_path))
#         return []
#
#     def get_target(self, pacman_x, pacman_y, pacman_direction, blinky_x, blinky_y):
#         if self.behavior == 'scatter':
#             return self.scatter_targets[self.name]
#         elif self.behavior == 'frightened':
#             if random.random() < 0.5:
#                 available = [(x, y) for x in range(GameConfig.MAP_WIDTH) for y in range(GameConfig.MAP_HEIGHT) if MAP_DATA[y][x] != 1]
#                 return random.choice(available)
#             dx = self.x - pacman_x
#             dy = self.y - pacman_y
#             target_x = self.x + dx
#             target_y = self.y + dy
#             target_x = max(0, min(GameConfig.MAP_WIDTH - 1, target_x))
#             target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, target_y))
#             return (target_x, target_y)
#         else:
#             if self.name == 'Blinky':
#                 return (pacman_x, pacman_y)
#             elif self.name == 'Pinky':
#                 dx, dy = DIRECTIONS[pacman_direction]
#                 target_x = pacman_x + dx * 4
#                 target_y = pacman_y + dy * 4
#                 target_x = max(0, min(GameConfig.MAP_WIDTH - 1, target_x))
#                 target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, target_y))
#                 return (target_x, target_y)
#             else:
#                 dx, dy = DIRECTIONS[pacman_direction]
#                 intermediate_x = pacman_x + dx * 2
#                 intermediate_y = pacman_y + dy * 2
#                 target_x = blinky_x + 2 * (intermediate_x - blinky_x)
#                 target_y = blinky_y + 2 * (intermediate_y - blinky_y)
#                 target_x = max(0, min(GameConfig.MAP_WIDTH - 1, target_x))
#                 target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, target_y))
#                 return (target_x, target_y)
#
#     def update(self, pacman_x, pacman_y, pacman_direction, blinky_x, blinky_y):
#         try:
#             logging.debug(f"{self.name}: x={self.x:.2f}, y={self.y:.2f}, behavior={self.behavior}, direction={self.direction}")
#             if self.behavior == 'frightened':
#                 self.frightened_timer -= 1
#                 if self.frightened_timer <= 0:
#                     self.behavior = 'chase'
#             if abs(self.x - round(self.x)) < 0.01 and abs(self.y - round(self.y)) < 0.01:
#                 self.target = self.get_target(pacman_x, pacman_y, pacman_direction, blinky_x, blinky_y)
#                 logging.debug(f"{self.name}: Новая цель={self.target}")
#                 self.path = self.a_star(self.x, self.y, self.target[0], self.target[1])
#                 if self.path:
#                     self.direction = self.path[0]
#                 else:
#                     available = self.get_available_directions()
#                     if available:
#                         self.direction = random.choice(available)
#                     else:
#                         logging.warning(f"{self.name}: Нет доступных направлений на ({self.x:.2f}, {self.y:.2f})")
#             dx, dy = DIRECTIONS[self.direction]
#             new_x = self.x + dx * self.speed
#             new_y = self.y + dy * self.speed
#             if self.can_move_to(new_x, new_y):
#                 self.x, self.y = new_x, new_y
#                 logging.debug(f"{self.name}: Двигается в {self.direction}, новая позиция ({self.x:.2f}, {self.y:.2f})")
#             else:
#                 self.x, self.y = round(self.x), round(self.y)
#                 logging.warning(f"{self.name}: Столкнулся с препятствием на ({self.x:.2f}, {self.y:.2f}), пересчёт пути")
#                 self.path = self.a_star(self.x, self.y, self.target[0], self.target[1])
#                 if self.path:
#                     self.direction = self.path[0]
#                 else:
#                     available = self.get_available_directions()
#                     if available:
#                         self.direction = random.choice(available)
#             if self.x < -0.5:
#                 self.x = GameConfig.MAP_WIDTH - 0.5
#             elif self.x >= GameConfig.MAP_WIDTH + 0.5:
#                 self.x = -0.5
#         except Exception as e:
#             logging.error(f"Ошибка обновления призрака {self.name}: {e}")
#
#     def draw(self, painter):
#         try:
#             size = GameConfig.CELL_SIZE
#             x = int(self.x * size)
#             y = int(self.y * size)
#             if self.behavior == 'frightened':
#                 gradient = QLinearGradient(x, y, x, y + size)
#                 gradient.setColorAt(0, QColor(0, 0, 255))
#                 gradient.setColorAt(1, QColor(0, 0, 180))
#             else:
#                 gradient = QLinearGradient(x, y, x, y + size)
#                 gradient.setColorAt(0, self.color.lighter(130))
#                 gradient.setColorAt(1, self.color.darker(130))
#             painter.setBrush(QBrush(gradient))
#             path = QPainterPath()
#             path.addEllipse(x, y, size, size * 0.8)
#             path.addRect(x, y + size * 0.4, size, size * 0.6)
#             painter.drawPath(path)
#             points = [
#                 QPoint(x, y + size),
#                 QPoint(x + size // 4, y + size - size // 8),
#                 QPoint(x + size // 2, y + size),
#                 QPoint(x + 3 * size // 4, y + size - size // 8),
#                 QPoint(x + size, y + size)
#             ]
#             painter.setPen(QPen(self.color.darker(150), 2))
#             painter.drawPolyline(QPolygon(points))
#             painter.setBrush(QBrush(QColor(255, 255, 255)))
#             white_eye_x1 = int(x + size * 0.3)
#             white_eye_y1 = int(y + size * 0.2)
#             white_eye_x2 = int(x + size * 0.5)
#             white_eye_y2 = int(y + size * 0.2)
#             painter.drawEllipse(white_eye_x1, white_eye_y1, int(size * 0.2), int(size * 0.2))
#             painter.drawEllipse(white_eye_x2, white_eye_y2, int(size * 0.2), int(size * 0.2))
#             painter.setBrush(QBrush(QColor(0, 0, 255)))
#             eye_dir = {'up': (0, -0.05), 'down': (0, 0.05), 'left': (-0.05, 0), 'right': (0.05, 0)}[self.direction]
#             eye_x = int(x + size * (0.35 + eye_dir[0]))
#             eye_y = int(y + size * (0.25 + eye_dir[1]))
#             painter.drawEllipse(eye_x, eye_y, int(size * 0.1), int(size * 0.1))
#             eye_x = int(x + size * (0.55 + eye_dir[0]))
#             eye_y = int(y + size * (0.25 + eye_dir[1]))
#             painter.drawEllipse(eye_x, eye_y, int(size * 0.1), int(size * 0.1))
#             # Свечение призрака
#             painter.setOpacity(0.5)
#             painter.setBrush(QBrush(self.color.lighter(150)))
#             painter.setPen(Qt.PenStyle.NoPen)
#             painter.drawEllipse(x - size * 0.1, y - size * 0.1, size * 1.2, size * 1.2)
#             painter.setOpacity(1.0)
#         except Exception as e:
#             logging.error(f"Ошибка отрисовки призрака: {e}")
#
# class PacmanGame(QWidget):
#     def __init__(self):
#         super().__init__()
#         try:
#             self.setWindowTitle("Pac-Man")
#             screen = QApplication.primaryScreen().geometry()
#             scale_factor = min(screen.width() / (GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE),
#                                screen.height() / (GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE))
#             GameConfig.CELL_SIZE = int(GameConfig.CELL_SIZE * scale_factor)
#             self.setFixedSize(screen.width(), screen.height())
#             self.offset_x = (screen.width() - GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE) // 2
#             self.offset_y = (screen.height() - GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE) // 2
#             self.game_state = 'start'
#             self.game_mode = 'scatter'
#             self.mode_timer = 0
#             self.pacman_x = 14
#             self.pacman_y = 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.score = 0
#             self.lives = 3
#             self.pellets_eaten = 0
#             self.ghosts = [
#                 Ghost(13.5, 11, QColor(255, 0, 0), 'Blinky'),
#                 Ghost(14.5, 11, QColor(255, 184, 255), 'Pinky'),
#                 Ghost(13.5, 13, QColor(0, 255, 255), 'Inky')
#             ]
#             self.stars = []
#             width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
#             height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
#             for i in range(200):
#                 x = random.randint(0, width - 1)
#                 y = random.randint(0, height - 1)
#                 brightness = random.randint(50, 255)
#                 speed = random.uniform(0.2, 0.8) * random.choice([-1, 1])
#                 size = random.randint(2, 5)
#                 self.stars.append(Star(x, y, brightness, speed, size))
#             self.timer = QTimer()
#             self.timer.timeout.connect(self.game_loop)
#             self.timer.setInterval(1000 // GameConfig.FPS)
#             self.timer.start()
#             self.pacman_animation_frame = 0
#             self.screen_animation_frame = 0
#             self.original_map = [row[:] for row in MAP_DATA]
#             self.showFullScreen()
#         except Exception as e:
#             logging.error(f"Ошибка инициализации: {e}")
#             sys.exit(1)
#
#     def keyPressEvent(self, event):
#         try:
#             key = event.key()
#             if self.game_state == 'start':
#                 if key == Qt.Key.Key_Space:
#                     self.game_state = 'playing'
#                     self.update()
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#             elif self.game_state == 'playing':
#                 if key == Qt.Key.Key_Left:
#                     self.next_direction = 'left'
#                 elif key == Qt.Key.Key_Right:
#                     self.next_direction = 'right'
#                 elif key == Qt.Key.Key_Up:
#                     self.next_direction = 'up'
#                 elif key == Qt.Key.Key_Down:
#                     self.next_direction = 'down'
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#             elif self.game_state in ['game_over', 'win']:
#                 if key == Qt.Key.Key_Space:
#                     self.reset_game()
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#         except Exception as e:
#             logging.error(f"Ошибка обработки нажатия клавиши: {e}")
#
#     def can_move_to(self, x, y):
#         try:
#             grid_x = int(round(x))
#             grid_y = int(round(y))
#             return (0 <= grid_x < GameConfig.MAP_WIDTH and
#                     0 <= grid_y < GameConfig.MAP_HEIGHT and
#                     MAP_DATA[grid_y][grid_x] != 1)
#         except Exception as e:
#             logging.error(f"Ошибка проверки движения: {e}")
#             return False
#
#     def move_pacman(self):
#         try:
#             at_intersection = (
#                 abs(self.pacman_x - round(self.pacman_x)) < GameConfig.PACMAN_SPEED * 2 and
#                 abs(self.pacman_y - round(self.pacman_y)) < GameConfig.PACMAN_SPEED * 2
#             )
#             if at_intersection:
#                 test_x, test_y = int(self.pacman_x), int(self.pacman_y)
#                 test_move_x, test_move_y = DIRECTIONS[self.next_direction]
#                 if self.can_move_to(test_x + test_move_x, test_y + test_move_y):
#                     self.pacman_direction = self.next_direction
#             dx, dy = DIRECTIONS[self.pacman_direction]
#             new_x = self.pacman_x + dx * GameConfig.PACMAN_SPEED
#             new_y = self.pacman_y + dy * GameConfig.PACMAN_SPEED
#             if self.can_move_to(new_x, new_y):
#                 self.pacman_x, self.pacman_y = new_x, new_y
#             else:
#                 self.pacman_x = round(self.pacman_x)
#                 self.pacman_y = round(self.pacman_y)
#             if self.pacman_x < -0.5:
#                 self.pacman_x = GameConfig.MAP_WIDTH - 0.5
#             elif self.pacman_x >= GameConfig.MAP_WIDTH + 0.5:
#                 self.pacman_x = -0.5
#         except Exception as e:
#             logging.error(f"Ошибка движения Пакмана: {e}")
#
#     def check_collisions(self):
#         try:
#             for ghost in self.ghosts:
#                 if (abs(self.pacman_x - ghost.x) < 0.35 and
#                         abs(self.pacman_y - ghost.y) < 0.35):
#                     if ghost.behavior == 'frightened':
#                         ghost.behavior = 'chase'
#                         ghost.x, ghost.y = ghost.home_x, ghost.home_y
#                         self.score += 200
#                     else:
#                         self.lives -= 1
#                         if self.lives <= 0:
#                             self.game_state = 'game_over'
#                         else:
#                             self.reset_positions()
#         except Exception as e:
#             logging.error(f"Ошибка проверки столкновений: {e}")
#
#     def eat_dots(self):
#         try:
#             x, y = int(self.pacman_x), int(self.pacman_y)
#             cell = MAP_DATA[y][x]
#             if cell == 2:
#                 MAP_DATA[y][x] = 0
#                 self.score += 10
#                 self.pellets_eaten += 1
#             elif cell == 3:
#                 MAP_DATA[y][x] = 0
#                 self.score += 50
#                 self.pellets_eaten += 1
#                 for ghost in self.ghosts:
#                     ghost.behavior = 'frightened'
#                     ghost.frightened_timer = GameConfig.MODE_DURATIONS['frightened'] * GameConfig.FPS
#             if self.pellets_eaten >= GameConfig.TOTAL_PELLETS:
#                 self.game_state = 'win'
#         except Exception as e:
#             logging.error(f"Ошибка поедания точек: {e}")
#
#     def reset_positions(self):
#         try:
#             self.pacman_x, self.pacman_y = 14, 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.ghosts[0].x, self.ghosts[0].y = 13.5, 11
#             self.ghosts[1].x, self.ghosts[1].y = 14.5, 11
#             self.ghosts[2].x, self.ghosts[2].y = 13.5, 13
#             for ghost in self.ghosts:
#                 ghost.behavior = 'chase'
#                 ghost.path = []
#                 ghost.direction = 'right'
#                 ghost.target = ghost.scatter_targets[ghost.name]
#         except Exception as e:
#             logging.error(f"Ошибка сброса позиций: {e}")
#
#     def reset_game(self):
#         try:
#             self.game_state = 'playing'
#             self.game_mode = 'scatter'
#             self.mode_timer = 0
#             self.pacman_x = 14
#             self.pacman_y = 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.score = 0
#             self.lives = 3
#             self.pellets_eaten = 0
#             self.ghosts = [
#                 Ghost(13.5, 11, QColor(255, 0, 0), 'Blinky'),
#                 Ghost(14.5, 11, QColor(255, 184, 255), 'Pinky'),
#                 Ghost(13.5, 13, QColor(0, 255, 255), 'Inky')
#             ]
#             self.pacman_animation_frame = 0
#             self.screen_animation_frame = 0
#             for y in range(GameConfig.MAP_HEIGHT):
#                 for x in range(GameConfig.MAP_WIDTH):
#                     MAP_DATA[y][x] = self.original_map[y][x]
#             self.update()
#         except Exception as e:
#             logging.error(f"Ошибка сброса игры: {e}")
#
#     def game_loop(self):
#         try:
#             if self.game_state == 'playing':
#                 self.move_pacman()
#                 self.eat_dots()
#                 blinky_x = self.ghosts[0].x
#                 blinky_y = self.ghosts[0].y
#                 for ghost in self.ghosts:
#                     ghost.update(self.pacman_x, self.pacman_y, self.pacman_direction, blinky_x, blinky_y)
#                 self.check_collisions()
#                 self.mode_timer += 1
#                 if self.mode_timer >= GameConfig.MODE_DURATIONS[self.game_mode] * GameConfig.FPS:
#                     self.mode_timer = 0
#                     self.game_mode = 'chase' if self.game_mode == 'scatter' else 'scatter'
#                     for ghost in self.ghosts:
#                         if ghost.behavior != 'frightened':
#                             ghost.behavior = self.game_mode
#             for star in self.stars:
#                 star.update()
#             self.screen_animation_frame = (self.screen_animation_frame + 1) % 60
#             self.pacman_animation_frame = (self.pacman_animation_frame + 1) % 20
#             self.update()
#         except Exception as e:
#             logging.error(f"Ошибка игрового цикла: {e}")
#
#     def paintEvent(self, event):
#         try:
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#             width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
#             height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
#             painter.translate(self.offset_x, self.offset_y)
#
#             if self.game_state == 'start':
#                 # Радиальный градиент для фона
#                 gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
#                 gradient.setColorAt(0, QColor(20, 20, 80))
#                 gradient.setColorAt(1, QColor(0, 0, 0))
#                 painter.fillRect(0, 0, width, height, QBrush(gradient))
#
#                 # Звёзды
#                 for star in self.stars:
#                     painter.setOpacity(star.brightness / 255)
#                     painter.setBrush(QBrush(QColor(255, 255, 255)))
#                     painter.setPen(Qt.PenStyle.NoPen)
#                     painter.drawEllipse(star.x, star.y, star.size, star.size)
#                 painter.setOpacity(1.0)
#
#                 # Заголовок с неоновым свечением
#                 pulse = 1 + 0.15 * math.sin(self.screen_animation_frame * 0.15)
#                 painter.setFont(QFont('Arial', int(GameConfig.CELL_SIZE * 3.5 * pulse), QFont.Weight.Bold))
#                 for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#                     painter.setPen(QPen(QColor(255, 255, 0, 100)))
#                     painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE + offset[0],
#                                      height // 2 - 3 * GameConfig.CELL_SIZE + offset[1], "Pac-Man")
#                 painter.setPen(QPen(QColor(255, 255, 0)))
#                 painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE, height // 2 - 3 * GameConfig.CELL_SIZE, "Pac-Man")
#
#                 # Анимированный Pac-Man
#                 size = GameConfig.CELL_SIZE * 3
#                 pacman_x = width // 2 - size // 2 + int(50 * math.sin(self.screen_animation_frame * 0.1))
#                 pacman_y = height // 2
#                 gradient = QRadialGradient(pacman_x + size // 2, pacman_y + size // 2, size)
#                 gradient.setColorAt(0, QColor(255, 255, 0))
#                 gradient.setColorAt(1, QColor(200, 200, 0))
#                 painter.setBrush(QBrush(gradient))
#                 painter.setPen(Qt.PenStyle.NoPen)
#                 start_angle = 30 * 16
#                 span_angle = 300 * 16 if self.pacman_animation_frame < 10 else 360 * 16
#                 painter.drawPie(pacman_x, pacman_y, size, size, start_angle, span_angle)
#                 painter.setOpacity(0.4)
#                 painter.setBrush(QBrush(QColor(255, 255, 0, 100)))
#                 painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#                 painter.setOpacity(1.0)
#                 eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
#                 eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
#                 painter.setBrush(QBrush(QColor(0, 0, 0)))
#                 painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#
#                 # Полупрозрачная панель для инструкций
#                 painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#                 painter.setPen(Qt.PenStyle.NoPen)
#                 painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height - 3 * GameConfig.CELL_SIZE,
#                                         24 * GameConfig.CELL_SIZE, 2 * GameConfig.CELL_SIZE, 10, 10)
#                 painter.setFont(QFont('Arial', GameConfig.CELL_SIZE))
#                 painter.setPen(QPen(QColor(255, 255, 255)))
#                 opacity = 0.7 + 0.3 * math.sin(self.screen_animation_frame * 0.2)
#                 painter.setOpacity(opacity)
#                 painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height - 2 * GameConfig.CELL_SIZE,
#                                  "Нажми SPACE для старта")
#                 painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, height - GameConfig.CELL_SIZE,
#                                  "Стрелки: Двигаться | ESC: Выход")
#                 painter.setOpacity(1.0)
#
#             elif self.game_state == 'playing':
#                 gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
#                 gradient.setColorAt(0, QColor(20, 20, 80))
#                 gradient.setColorAt(1, QColor(0, 0, 0))
#                 painter.fillRect(0, 0, width, height, QBrush(gradient))
#                 for y in range(GameConfig.MAP_HEIGHT):
#                     for x in range(GameConfig.MAP_WIDTH):
#                         cell = MAP_DATA[y][x]
#                         rect_x = x * GameConfig.CELL_SIZE
#                         rect_y = y * GameConfig.CELL_SIZE
#                         if cell == 1:
#                             gradient = QLinearGradient(rect_x, rect_y, rect_x, rect_y + GameConfig.CELL_SIZE)
#                             gradient.setColorAt(0, QColor(0, 0, 240))
#                             gradient.setColorAt(1, QColor(0, 0, 180))
#                             painter.setBrush(QBrush(gradient))
#                             painter.setPen(QPen(QColor(0, 0, 255), 2))
#                             path = QPainterPath()
#                             path.addRoundedRect(QRectF(rect_x, rect_y, GameConfig.CELL_SIZE, GameConfig.CELL_SIZE), 5, 5)
#                             painter.drawPath(path)
#                         elif cell == 2:
#                             painter.setBrush(QBrush(QColor(255, 255, 200)))
#                             painter.setPen(Qt.PenStyle.NoPen)
#                             center_x = int(rect_x + GameConfig.CELL_SIZE // 2)
#                             center_y = int(rect_y + GameConfig.CELL_SIZE // 2)
#                             painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)
#                         elif cell == 3:
#                             painter.setBrush(QBrush(QColor(255, 255, 200)))
#                             painter.setPen(Qt.PenStyle.NoPen)
#                             pulse = 8 + 2 * math.sin(self.pacman_animation_frame * 0.3)
#                             center_x = int(rect_x + GameConfig.CELL_SIZE // 2)
#                             center_y = int(rect_y + GameConfig.CELL_SIZE // 2)
#                             size = int(pulse * 2)
#                             painter.drawEllipse(center_x - size // 2, center_y - size // 2, size, size)
#                 for ghost in self.ghosts:
#                     ghost.draw(painter)
#                 size = GameConfig.CELL_SIZE
#                 x = int(self.pacman_x * size)
#                 y = int(self.pacman_y * size)
#                 gradient = QRadialGradient(x + size // 2, y + size // 2, size)
#                 gradient.setColorAt(0, QColor(255, 255, 0))
#                 gradient.setColorAt(1, QColor(200, 200, 0))
#                 painter.setBrush(QBrush(gradient))
#                 painter.setPen(Qt.PenStyle.NoPen)
#                 start_angle = {'right': 30, 'left': 210, 'up': 300, 'down': 120}[self.pacman_direction] * 16
#                 span_angle = 300 * 16
#                 if self.pacman_animation_frame < 10:
#                     span_angle = 360 * 16
#                 elif self.pacman_animation_frame < 15:
#                     span_angle = 330 * 16
#                 painter.drawPie(x, y, size, size, start_angle, span_angle)
#                 painter.setOpacity(0.4)
#                 painter.setBrush(QBrush(QColor(255, 255, 0, 100)))
#                 painter.drawEllipse(x - size * 0.2, y - size * 0.2, size * 1.4, size * 1.4)
#                 painter.setOpacity(1.0)
#                 eye_x = x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
#                 eye_y = y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
#                 painter.setBrush(QBrush(QColor(0, 0, 0)))
#                 painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#                 painter.setPen(QPen(QColor(255, 255, 255)))
#                 painter.setFont(QFont('Arial', GameConfig.CELL_SIZE // 2))
#                 painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#                 painter.drawRect(0, 0, width, int(GameConfig.CELL_SIZE * 1.5))
#                 painter.drawText(10, GameConfig.CELL_SIZE, f"Очки: {self.score}")
#                 painter.drawText(width - 10 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE, f"Жизни: {self.lives}")
#
#             elif self.game_state in ['game_over', 'win']:
#                 star_color = QColor(255, 255, 255)
#                 gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
#                 if self.game_state == 'game_over':
#                     gradient.setColorAt(0, QColor(80, 0, 0))
#                     gradient.setColorAt(1, QColor(20, 0, 0))
#                     star_color = QColor(255, 0, 0)
#                     text = "ИГРА ОКОНЧЕНА"
#                 else:
#                     gradient.setColorAt(0, QColor(0, 80, 0))
#                     gradient.setColorAt(1, QColor(0, 20, 0))
#                     star_color = QColor(0, 255, 0)
#                     text = "ПОБЕДА!"
#                 painter.fillRect(0, 0, width, height, QBrush(gradient))
#                 for star in self.stars:
#                     painter.setOpacity(star.brightness / 255)
#                     painter.setBrush(QBrush(star_color))
#                     painter.setPen(Qt.PenStyle.NoPen)
#                     painter.drawEllipse(star.x, star.y, star.size, star.size)
#                 painter.setOpacity(1.0)
#                 size = GameConfig.CELL_SIZE * 4
#                 pacman_x = width // 2 - size // 2
#                 pacman_y = height // 2 - size + int(20 * math.sin(self.screen_animation_frame * 0.2))
#                 if self.game_state == 'game_over':
#                     gradient = QRadialGradient(pacman_x + size // 2, pacman_y + size // 2, size)
#                     gradient.setColorAt(0, QColor(255, 255, 0))
#                     gradient.setColorAt(1, QColor(200, 200, 0))
#                     painter.setBrush(QBrush(gradient))
#                     painter.drawEllipse(pacman_x, pacman_y, size, size)
#                     painter.setOpacity(0.4)
#                     painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
#                     painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#                     painter.setOpacity(1.0)
#                     painter.setBrush(QBrush(QColor(0, 0, 0)))
#                     painter.drawEllipse(pacman_x + size // 4, pacman_y + size // 4, size // 4, size // 8)
#                     painter.drawEllipse(pacman_x + size // 2, pacman_y + size // 4, size // 4, size // 8)
#                     # Эффект "капель"
#                     painter.setPen(QPen(QColor(255, 0, 0), 2))
#                     for i in range(5):
#                         offset_y = int(20 * math.sin(self.screen_animation_frame * 0.1 + i))
#                         painter.drawLine(pacman_x + i * size // 5, pacman_y + size,
#                                          pacman_x + i * size // 5, pacman_y + size + offset_y)
#                 else:
#                     gradient = QRadialGradient(pacman_x + size // 2, pacman_y + size // 2, size)
#                     gradient.setColorAt(0, QColor(255, 255, 0))
#                     gradient.setColorAt(1, QColor(200, 200, 0))
#                     painter.setBrush(QBrush(gradient))
#                     painter.setPen(Qt.PenStyle.NoPen)
#                     painter.drawPie(pacman_x, pacman_y, size, size, 30 * 16, 300 * 16)
#                     painter.setOpacity(0.4)
#                     painter.setBrush(QBrush(QColor(255, 255, 0, 100)))
#                     painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#                     painter.setOpacity(1.0)
#                     eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(30)))
#                     eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(30)))
#                     painter.setBrush(QBrush(QColor(0, 0, 0)))
#                     painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#                     # Эффект искр
#                     painter.setBrush(QBrush(QColor(255, 255, 0)))
#                     for i in range(8):
#                         angle = self.screen_animation_frame * 0.2 + i * math.pi / 4
#                         spark_x = pacman_x + size // 2 + int(60 * math.cos(angle))
#                         spark_y = pacman_y + size // 2 + int(60 * math.sin(angle))
#                         painter.drawEllipse(spark_x - 3, spark_y - 3, 6, 6)
#                 painter.setFont(QFont('Arial', int(GameConfig.CELL_SIZE * 2.5), QFont.Weight.Bold))
#                 pulse = 1 + 0.15 * math.sin(self.screen_animation_frame * 0.15)
#                 color = QColor(255, 0, 0) if self.game_state == 'game_over' else QColor(0, 255, 0)
#                 for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#                     painter.setPen(QPen(color.lighter(150), 2))
#                     painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE + offset[0],
#                                      height // 2 - 4 * GameConfig.CELL_SIZE + offset[1], text)
#                 painter.setPen(QPen(color.lighter(100 + int(pulse * 50))))
#                 painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE, height // 2 - 4 * GameConfig.CELL_SIZE, text)
#                 painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#                 painter.setPen(Qt.PenStyle.NoPen)
#                 painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height // 2 - GameConfig.CELL_SIZE,
#                                         24 * GameConfig.CELL_SIZE, 3 * GameConfig.CELL_SIZE, 10, 10)
#                 painter.setFont(QFont('Arial', GameConfig.CELL_SIZE))
#                 painter.setPen(QPen(QColor(255, 255, 255)))
#                 opacity = 0.7 + 0.3 * math.sin(self.screen_animation_frame * 0.2)
#                 painter.setOpacity(opacity)
#                 painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height // 2, f"Очки: {self.score}")
#                 painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, height // 2 + GameConfig.CELL_SIZE,
#                                  "SPACE для рестарта | ESC для выхода")
#                 painter.setOpacity(1.0)
#
#         except Exception as e:
#             logging.error(f"Ошибка отрисовки: {e}")
#
# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         game = PacmanGame()
#         sys.exit(app.exec())
#     except Exception as e:
#         logging.error(f"Ошибка приложения: {e}")
#         print(f"Не удалось запустить игру: {e}")


# import sys
# import random
# import math
# import os
# import logging
# from PyQt6.QtWidgets import QApplication, QWidget
# from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPolygon, QBrush, QPainterPath, QRadialGradient, QLinearGradient
# from PyQt6.QtCore import QPoint, Qt, QTimer, QCoreApplication, QRectF
# from heapq import heappush, heappop
# from enum import Enum
#
# # Настройка логирования с дополнительной информацией для отладки
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
#     os.path.dirname(QCoreApplication.applicationFilePath()), 'Qt', 'plugins'
# )
#
# class GameState(Enum):
#     """Перечисление состояний игры."""
#     START = "start"
#     PLAYING = "playing"
#     PAUSED = "paused"
#     GAME_OVER = "game_over"
#     WIN = "win"
#
# class GameConfig:
#     """Конфигурация игры с константами."""
#     CELL_SIZE = 20
#     MAP_WIDTH = 28
#     MAP_HEIGHT = 31
#     FPS = 60
#     GHOST_SPEED = 0.2  # Увеличена базовая скорость призраков
#     PACMAN_SPEED = 0.2  # Увеличена скорость Pac-Man
#     PACMAN_BOOST_SPEED = 0.24  # Скорость с ускорением
#     MODE_DURATIONS = {'scatter': 7, 'chase': 20, 'frightened': 10}
#     TOTAL_PELLETS = 244
#     FONT = "Arial"
#     PRIMARY_COLOR = QColor(255, 255, 0)  # Pac-Man yellow
#     SECONDARY_COLOR = QColor(20, 20, 80)  # Background blue
#     WALL_COLOR = QColor(0, 0, 240)
#     PELLET_COLOR = QColor(255, 255, 200)
#     POWER_PELLET_COLOR = QColor(255, 200, 100)
#     FRUIT_COLOR = QColor(255, 0, 0)  # Cherry red
#     GLOW_OPACITY = 0.4
#     ANIMATION_SPEED = 0.2
#     HIGH_SCORE_FILE = "highscore.txt"
#     FRUIT_SCORE = 100
#     BOOST_DURATION = 5 * FPS  # 5 секунд ускорения
#     FRUIT_SPAWN_INTERVAL = 50  # Фрукт появляется каждые 50 точек
#
# # Карта игры
# MAP_DATA = [
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
#     [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
#     [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,1,2,1,1,1,1,1,2,0,0,2,1,1,1,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,0,2,0,0,0,1,0,2,0,0,2,0,1,0,0,0,2,0,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,1,1,1],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
#     [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
#     [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
#     [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
#     [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
#     [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
#     [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
#     [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
#     [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
#     [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# ]
#
# DIRECTIONS = {
#     'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)
# }
#
# class Star:
#     """Класс для анимированных частиц фона."""
#     def __init__(self, x, y, brightness, speed, size):
#         self.x = x
#         self.y = y
#         self.brightness = brightness
#         self.speed = speed
#         self.size = size
#
#     def update(self):
#         """Обновляет яркость частицы для создания эффекта мерцания."""
#         self.brightness += self.speed
#         if self.brightness > 255:
#             self.brightness = 255
#             self.speed = -self.speed
#         elif self.brightness < 50:
#             self.brightness = 50
#             self.speed = -self.speed
#
# class Ghost:
#     """Класс для управления призраками."""
#     def __init__(self, x, y, color, name):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.name = name
#         self.behavior = 'chase'
#         self.direction = 'right'
#         self.frightened_timer = 0
#         self.home_x = x
#         self.home_y = y
#         self.speed = GameConfig.GHOST_SPEED
#         self.scatter_targets = {
#             'Blinky': (26, 1), 'Pinky': (1, 1), 'Inky': (26, 29)
#         }
#         self.target = self.scatter_targets[name]
#         self.path = []
#         logging.info(f"Инициализация призрака {self.name} на позиции ({self.x}, {self.y})")
#
#     def can_move_to(self, x, y):
#         """Проверяет, можно ли переместиться в указанную клетку."""
#         grid_x, grid_y = int(round(x)), int(round(y))
#         return (0 <= grid_x < GameConfig.MAP_WIDTH and
#                 0 <= grid_y < GameConfig.MAP_HEIGHT and
#                 MAP_DATA[grid_y][grid_x] != 1)
#
#     def get_available_directions(self):
#         """Возвращает список доступных направлений движения."""
#         return [d for d, (dx, dy) in DIRECTIONS.items() if self.can_move_to(self.x + dx, self.y + dy)]
#
#     def get_opposite_direction(self, direction):
#         """Возвращает противоположное направление."""
#         opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
#         return opposites.get(direction, direction)
#
#     def is_in_corridor(self, pacman_x, pacman_y):
#         """Проверяет, находится ли Pac-Man в узком коридоре (для ловушек)."""
#         x, y = int(pacman_x), int(pacman_y)
#         exits = 0
#         for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < GameConfig.MAP_WIDTH and 0 <= ny < GameConfig.MAP_HEIGHT and MAP_DATA[ny][nx] != 1:
#                 exits += 1
#         return exits <= 2
#
#     def a_star(self, start_x, start_y, target_x, target_y, avoid_dead_ends=False):
#         """Реализует алгоритм A* с учётом избегания тупиков."""
#         start_x, start_y = int(round(start_x)), int(round(start_y))
#         target_x, target_y = int(round(target_x)), int(round(target_y))
#         open_set = [(0, start_x, start_y, [])]
#         closed_set = set()
#         g_score = {(start_x, start_y): 0}
#         f_score = {(start_x, start_y): abs(target_x - start_x) + abs(target_y - start_y)}
#
#         while open_set:
#             _, x, y, path = heappop(open_set)
#             if (x, y) == (target_x, target_y):
#                 return path
#             if (x, y) in closed_set:
#                 continue
#             closed_set.add((x, y))
#             for direction, (dx, dy) in DIRECTIONS.items():
#                 next_x, next_y = x + dx, y + dy
#                 if not self.can_move_to(next_x, next_y):
#                     continue
#                 if avoid_dead_ends:
#                     available_dirs = sum(1 for d, (ndx, ndy) in DIRECTIONS.items()
#                                         if self.can_move_to(next_x + ndx, next_y + ndy))
#                     if available_dirs <= 1:  # Пропускаем тупики
#                         continue
#                 tentative_g_score = g_score[(x, y)] + 1
#                 if (next_x, next_y) not in g_score or tentative_g_score < g_score[(next_x, next_y)]:
#                     g_score[(next_x, next_y)] = tentative_g_score
#                     f_score[(next_x, next_y)] = tentative_g_score + abs(target_x - next_x) + abs(target_y - next_y)
#                     heappush(open_set, (f_score[(next_x, next_y)], next_x, next_y, path + [direction]))
#         return []
#
#     def get_target(self, pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y):
#         """Определяет цель для призрака с учётом предсказания движения Pac-Man."""
#         if self.behavior == 'scatter':
#             return self.scatter_targets[self.name]
#         elif self.behavior == 'frightened':
#             if random.random() < 0.5:
#                 available = [(x, y) for x in range(GameConfig.MAP_WIDTH) for y in range(GameConfig.MAP_HEIGHT)
#                              if MAP_DATA[y][x] != 1]
#                 return random.choice(available)
#             dx, dy = self.x - pacman_x, self.y - pacman_y
#             target_x = max(0, min(GameConfig.MAP_WIDTH - 1, self.x + dx))
#             target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, self.y + dy))
#             return (target_x, target_y)
#         else:
#             # Проверяем, в коридоре ли Pac-Man, для установки ловушки
#             trap_mode = self.is_in_corridor(pacman_x, pacman_y) and random.random() < 0.3
#             if trap_mode:
#                 # Выбираем позицию, блокирующую выход из коридора
#                 exits = [(pacman_x + dx, pacman_y + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
#                          if self.can_move_to(pacman_x + dx, pacman_y + dy)]
#                 if exits:
#                     return random.choice(exits)
#             if self.name == 'Blinky':
#                 return (pacman_x, pacman_y)
#             elif self.name == 'Pinky':
#                 # Предсказываем движение на 6 клеток вперёд
#                 dx, dy = DIRECTIONS.get(next_direction, DIRECTIONS[pacman_direction])
#                 target_x = max(0, min(GameConfig.MAP_WIDTH - 1, pacman_x + dx * 6))
#                 target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, pacman_y + dy * 6))
#                 return (target_x, target_y)
#             else:  # Inky
#                 # Зажимаем Pac-Man, используя позицию Blinky
#                 dx, dy = DIRECTIONS.get(next_direction, DIRECTIONS[pacman_direction])
#                 intermediate_x = pacman_x + dx * 2
#                 intermediate_y = pacman_y + dy * 2
#                 target_x = max(0, min(GameConfig.MAP_WIDTH - 1, blinky_x + 2 * (intermediate_x - blinky_x)))
#                 target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, blinky_y + 2 * (intermediate_y - blinky_y)))
#                 return (target_x, target_y)
#
#     def update(self, pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y):
#         """Обновляет позицию и поведение призрака."""
#         try:
#             if self.behavior == 'frightened':
#                 self.frightened_timer -= 1
#                 if self.frightened_timer <= 0:
#                     self.behavior = 'chase'
#             if abs(self.x - round(self.x)) < 0.01 and abs(self.y - round(self.y)) < 0.01:
#                 self.target = self.get_target(pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y)
#                 avoid_dead_ends = self.name == 'Blinky'  # Blinky избегает тупиков
#                 if not self.path:
#                     self.path = self.a_star(self.x, self.y, self.target[0], self.target[1], avoid_dead_ends)
#                 if self.path:
#                     self.direction = self.path.pop(0)
#                 else:
#                     available = self.get_available_directions()
#                     if available:
#                         self.direction = random.choice(available)
#             dx, dy = DIRECTIONS[self.direction]
#             new_x, new_y = self.x + dx * self.speed, self.y + dy * self.speed
#             if self.can_move_to(new_x, new_y):
#                 self.x, self.y = new_x, new_y
#             else:
#                 self.x, self.y = round(self.x), round(self.y)
#                 self.path = self.a_star(self.x, self.y, self.target[0], self.target[1], avoid_dead_ends)
#                 if self.path:
#                     self.direction = self.path.pop(0)
#                 else:
#                     available = self.get_available_directions()
#                     if available:
#                         self.direction = random.choice(available)
#             if self.x < -0.5:
#                 self.x = GameConfig.MAP_WIDTH - 0.5
#             elif self.x >= GameConfig.MAP_WIDTH + 0.5:
#                 self.x = -0.5
#             logging.debug(f"Призрак {self.name}: позиция ({self.x:.2f}, {self.y:.2f}), направление {self.direction}")
#         except Exception as e:
#             logging.error(f"Ошибка обновления призрака {self.name}: {e}")
#
#     def draw(self, painter):
#         """Отрисовывает призрака с градиентной заливкой и эффектом свечения."""
#         try:
#             size = GameConfig.CELL_SIZE
#             x = int(self.x * size)
#             y = int(self.y * size)
#             gradient = QLinearGradient(x, y, x, y + size)
#             if self.behavior == 'frightened':
#                 gradient.setColorAt(0, QColor(0, 0, 255))
#                 gradient.setColorAt(1, QColor(0, 0, 180))
#             else:
#                 gradient.setColorAt(0, self.color.lighter(130))
#                 gradient.setColorAt(1, self.color.darker(130))
#             painter.setBrush(QBrush(gradient))
#             path = QPainterPath()
#             path.addEllipse(x, y, size, size * 0.8)
#             path.addRect(x, y + size * 0.4, size, size * 0.6)
#             painter.drawPath(path)
#             points = [
#                 QPoint(x, y + size),
#                 QPoint(x + size // 4, y + size - size // 8),
#                 QPoint(x + size // 2, y + size),
#                 QPoint(x + 3 * size // 4, y + size - size // 8),
#                 QPoint(x + size, y + size)
#             ]
#             painter.setPen(QPen(self.color.darker(150), 2))
#             painter.drawPolyline(QPolygon(points))
#             painter.setBrush(QBrush(QColor(255, 255, 255)))
#             eye_dir = {'up': (0, -0.05), 'down': (0, 0.05), 'left': (-0.05, 0), 'right': (0.05, 0)}[self.direction]
#             for offset in [(0.3, 0.2), (0.5, 0.2)]:
#                 white_eye_x = int(x + size * offset[0])
#                 white_eye_y = int(y + size * offset[1])
#                 painter.drawEllipse(white_eye_x, white_eye_y, int(size * 0.2), int(size * 0.2))
#                 eye_x = int(x + size * (offset[0] + 0.05 + eye_dir[0]))
#                 eye_y = int(y + size * (offset[1] + 0.05 + eye_dir[1]))
#                 painter.setBrush(QBrush(QColor(0, 0, 255)))
#                 painter.drawEllipse(eye_x, eye_y, int(size * 0.1), int(size * 0.1))
#             painter.setOpacity(GameConfig.GLOW_OPACITY)
#             painter.setBrush(QBrush(self.color.lighter(150)))
#             painter.setPen(Qt.PenStyle.NoPen)
#             painter.drawEllipse(x - size * 0.1, y - size * 0.1, size * 1.2, size * 1.2)
#             painter.setOpacity(1.0)
#         except Exception as e:
#             logging.error(f"Ошибка отрисовки призрака {self.name}: {e}")
#
# class HighScoreManager:
#     """Класс для управления рекордами."""
#     def __init__(self):
#         self.high_score = self.load_high_score()
#
#     def load_high_score(self):
#         """Загружает рекорд из файла."""
#         try:
#             with open(GameConfig.HIGH_SCORE_FILE, 'r') as f:
#                 return int(f.read() or 0)
#         except (FileNotFoundError, ValueError):
#             return 0
#
#     def save_high_score(self, score):
#         """Сохраняет рекорд, если текущий счёт выше."""
#         if score > self.high_score:
#             self.high_score = score
#             try:
#                 with open(GameConfig.HIGH_SCORE_FILE, 'w') as f:
#                     f.write(str(score))
#             except Exception as e:
#                 logging.error(f"Ошибка сохранения рекорда: {e}")
#
# class GameStateManager:
#     """Класс для управления состоянием игры."""
#     def __init__(self):
#         self.state = GameState.START
#         self.mode = 'scatter'
#         self.mode_timer = 0
#         self.score = 0
#         self.lives = 3
#         self.pellets_eaten = 0
#         self.level = 1
#         self.fruit_active = False
#         self.fruit_x = 0
#         self.fruit_y = 0
#         self.boost_timer = 0
#
#     def switch_mode(self):
#         """Переключает режим игры (scatter/chase)."""
#         self.mode_timer += 1
#         if self.mode_timer >= GameConfig.MODE_DURATIONS[self.mode] * GameConfig.FPS:
#             self.mode_timer = 0
#             self.mode = 'chase' if self.mode == 'scatter' else 'scatter'
#
#     def reset(self):
#         """Сбрасывает состояние игры."""
#         self.state = GameState.PLAYING
#         self.mode = 'scatter'
#         self.mode_timer = 0
#         self.score = 0
#         self.lives = 3
#         self.pellets_eaten = 0
#         self.level = 1
#         self.fruit_active = False
#         self.boost_timer = 0
#
# class Renderer:
#     """Класс для отрисовки игровых элементов."""
#     def __init__(self, game):
#         self.game = game
#         width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
#         height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
#         self.stars = [Star(random.randint(0, width - 1),
#                           random.randint(0, height - 1),
#                           random.randint(50, 255),
#                           random.uniform(0.2, 0.8) * random.choice([-1, 1]),
#                           random.randint(2, 5)) for _ in range(200)]
#
#     def draw_background(self, painter, width, height):
#         """Отрисовывает фон с радиальным градиентом и звёздами."""
#         gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
#         gradient.setColorAt(0, GameConfig.SECONDARY_COLOR)
#         gradient.setColorAt(1, QColor(0, 0, 0))
#         painter.fillRect(0, 0, width, height, QBrush(gradient))
#         for star in self.stars:
#             star.update()
#             painter.setOpacity(star.brightness / 255)
#             painter.setBrush(QBrush(QColor(255, 255, 255)))
#             painter.setPen(Qt.PenStyle.NoPen)
#             painter.drawEllipse(star.x, star.y, star.size, star.size)
#         painter.setOpacity(1.0)
#
#     def draw_map(self, painter):
#         """Отрисовывает карту с неоновыми стенами, точками и фруктами."""
#         for y in range(GameConfig.MAP_HEIGHT):
#             for x in range(GameConfig.MAP_WIDTH):
#                 cell = MAP_DATA[y][x]
#                 rect_x, rect_y = x * GameConfig.CELL_SIZE, y * GameConfig.CELL_SIZE
#                 if cell == 1:
#                     gradient = QLinearGradient(rect_x, rect_y, rect_x, rect_y + GameConfig.CELL_SIZE)
#                     gradient.setColorAt(0, GameConfig.WALL_COLOR.lighter(130))
#                     gradient.setColorAt(1, GameConfig.WALL_COLOR.darker(130))
#                     painter.setBrush(QBrush(gradient))
#                     painter.setPen(QPen(GameConfig.WALL_COLOR, 2))
#                     path = QPainterPath()
#                     path.addRoundedRect(QRectF(rect_x, rect_y, GameConfig.CELL_SIZE, GameConfig.CELL_SIZE), 5, 5)
#                     painter.drawPath(path)
#                     painter.setOpacity(GameConfig.GLOW_OPACITY)
#                     painter.setBrush(QBrush(GameConfig.WALL_COLOR.lighter(150)))
#                     painter.drawRoundedRect(QRectF(rect_x - 2, rect_y - 2, GameConfig.CELL_SIZE + 4, GameConfig.CELL_SIZE + 4), 5, 5)
#                     painter.setOpacity(1.0)
#                 elif cell == 2:
#                     painter.setBrush(QBrush(GameConfig.PELLET_COLOR))
#                     painter.setPen(Qt.PenStyle.NoPen)
#                     center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
#                     painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)
#                 elif cell == 3:
#                     pulse = 8 + 3 * math.sin(self.game.pacman_animation_frame * GameConfig.ANIMATION_SPEED * 1.5)
#                     painter.setBrush(QBrush(GameConfig.POWER_PELLET_COLOR))
#                     painter.setPen(Qt.PenStyle.NoPen)
#                     center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
#                     size = int(pulse * 2)
#                     painter.drawEllipse(center_x - size // 2, center_y - size // 2, size, size)
#                     # Вспышка для силовых точек
#                     painter.setOpacity(GameConfig.GLOW_OPACITY * (0.5 + 0.5 * math.sin(self.game.pacman_animation_frame * GameConfig.ANIMATION_SPEED)))
#                     painter.setBrush(QBrush(GameConfig.POWER_PELLET_COLOR.lighter(150)))
#                     painter.drawEllipse(center_x - size, center_y - size, size * 2, size * 2)
#                     painter.setOpacity(1.0)
#         # Отрисовка фрукта
#         if self.game.state_manager.fruit_active:
#             fruit_x, fruit_y = self.game.state_manager.fruit_x, self.game.state_manager.fruit_y
#             rect_x, rect_y = fruit_x * GameConfig.CELL_SIZE, fruit_y * GameConfig.CELL_SIZE
#             painter.setBrush(QBrush(GameConfig.FRUIT_COLOR))
#             painter.setPen(Qt.PenStyle.NoPen)
#             center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
#             painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)
#             # Визуальный эффект для фрукта
#             painter.setOpacity(GameConfig.GLOW_OPACITY)
#             painter.setBrush(QBrush(GameConfig.FRUIT_COLOR.lighter(150)))
#             painter.drawEllipse(center_x - 7, center_y - 7, 14, 14)
#             painter.setOpacity(1.0)
#
#     def draw_pacman(self, painter):
#         """Отрисовывает Pac-Man с анимированным ртом и эффектом свечения."""
#         try:
#             size = GameConfig.CELL_SIZE
#             x = int(self.game.pacman_x * size)
#             y = int(self.game.pacman_y * size)
#             logging.debug(f"Отрисовка Pac-Man на позиции ({x}, {y})")
#             gradient = QRadialGradient(x + size // 2, y + size // 2, size)
#             gradient.setColorAt(0, GameConfig.PRIMARY_COLOR)
#             gradient.setColorAt(1, GameConfig.PRIMARY_COLOR.darker(150))
#             painter.setBrush(QBrush(gradient))
#             painter.setPen(Qt.PenStyle.NoPen)
#             start_angle = {'right': 30, 'left': 210, 'up': 300, 'down': 120}.get(self.game.pacman_direction, 30) * 16
#             span_angle = 360 * 16 if self.game.pacman_animation_frame < 5 else (330 * 16 if self.game.pacman_animation_frame < 10 else 300 * 16)
#             painter.drawPie(x, y, size, size, start_angle, span_angle)
#             # Усиленное свечение при ускорении
#             glow_size = size * 1.4 if self.game.state_manager.boost_timer > 0 else size * 1.2
#             painter.setOpacity(GameConfig.GLOW_OPACITY)
#             painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150 + (50 if self.game.state_manager.boost_timer > 0 else 0))))
#             painter.drawEllipse(x - glow_size * 0.1, y - glow_size * 0.1, glow_size, glow_size)
#             painter.setOpacity(1.0)
#             eye_x = x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
#             eye_y = y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
#             painter.setBrush(QBrush(QColor(0, 0, 0)))
#             painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#         except Exception as e:
#             logging.error(f"Ошибка отрисовки Pac-Man: {e}")
#
#     def draw_hud(self, painter, width):
#         """Отрисовывает HUD с информацией об очках, жизнях, уровне и рекорде."""
#         painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.drawRect(0, 0, width, int(GameConfig.CELL_SIZE * 1.5))
#         painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE // 2))
#         painter.setPen(QPen(QColor(255, 255, 255)))
#         painter.drawText(10, GameConfig.CELL_SIZE, f"Очки: {self.game.state_manager.score}")
#         painter.drawText(width - 15 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE,
#                          f"Жизни: {self.game.state_manager.lives} | Уровень: {self.game.state_manager.level} | Рекорд: {self.game.high_score_manager.high_score}")
#         # Индикатор ускорения
#         if self.game.state_manager.boost_timer > 0:
#             painter.setPen(QPen(QColor(255, 255, 0)))
#             painter.drawText(width // 2 - 5 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE, "Ускорение!")
#
#     def draw_start_screen(self, painter, width, height):
#         """Отрисовывает стартовый экран с анимированным заголовком и Pac-Man."""
#         self.draw_background(painter, width, height)
#         pulse = 1 + 0.15 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
#         painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 3.5 * pulse), QFont.Weight.Bold))
#         for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#             painter.setPen(QPen(GameConfig.PRIMARY_COLOR.lighter(150), 2))
#             painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE + offset[0],
#                              height // 2 - 3 * GameConfig.CELL_SIZE + offset[1], "Pac-Man")
#         painter.setPen(QPen(GameConfig.PRIMARY_COLOR))
#         painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE, height // 2 - 3 * GameConfig.CELL_SIZE, "Pac-Man")
#         size = GameConfig.CELL_SIZE * 3
#         pacman_x = width // 2 - size // 2 + int(50 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED))
#         pacman_y = height // 2
#         gradient = QRadialGradient(pacman_x + size // 2, pacman_y + size // 2, size)
#         gradient.setColorAt(0, GameConfig.PRIMARY_COLOR)
#         gradient.setColorAt(1, GameConfig.PRIMARY_COLOR.darker(150))
#         painter.setBrush(QBrush(gradient))
#         painter.setPen(Qt.PenStyle.NoPen)
#         start_angle = 30 * 16
#         span_angle = 360 * 16 if self.game.pacman_animation_frame < 5 else (330 * 16 if self.game.pacman_animation_frame < 10 else 300 * 16)
#         painter.drawPie(pacman_x, pacman_y, size, size, start_angle, span_angle)
#         painter.setOpacity(GameConfig.GLOW_OPACITY)
#         painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150)))
#         painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#         painter.setOpacity(1.0)
#         eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
#         eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
#         painter.setBrush(QBrush(QColor(0, 0, 0)))
#         painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#         painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height - 3 * GameConfig.CELL_SIZE,
#                                 24 * GameConfig.CELL_SIZE, 2 * GameConfig.CELL_SIZE, 10, 10)
#         painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
#         painter.setPen(QPen(QColor(255, 255, 255)))
#         opacity = 0.7 + 0.3 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
#         painter.setOpacity(opacity)
#         painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height - 2 * GameConfig.CELL_SIZE,
#                          "Нажми SPACE для старта")
#         painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, height - GameConfig.CELL_SIZE,
#                          "Стрелки: Двигаться | P: Пауза | ESC: Выход")
#         painter.setOpacity(1.0)
#
#     def draw_game_over_win(self, painter, width, height):
#         """Отрисовывает экраны победы или поражения с анимациями."""
#         star_color = QColor(255, 255, 255)
#         text = "ПОБЕДА!" if self.game.state_manager.state == GameState.WIN else "ИГРА ОКОНЧЕНА"
#         text_color = QColor(0, 255, 0) if self.game.state_manager.state == GameState.WIN else QColor(255, 0, 0)
#         gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
#         gradient.setColorAt(0, text_color.darker(150))
#         gradient.setColorAt(1, QColor(0, 0, 0))
#         star_color = text_color
#         painter.fillRect(0, 0, width, height, QBrush(gradient))
#         for star in self.stars:
#             painter.setOpacity(star.brightness / 255)
#             painter.setBrush(QBrush(star_color))
#             painter.setPen(Qt.PenStyle.NoPen)
#             painter.drawEllipse(star.x, star.y, star.size, star.size)
#         painter.setOpacity(1.0)
#         size = GameConfig.CELL_SIZE * 4
#         pacman_x = width // 2 - size // 2
#         pacman_y = height // 2 - size + int(20 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED))
#         gradient = QRadialGradient(pacman_x + size // 2, pacman_y + size // 2, size)
#         gradient.setColorAt(0, GameConfig.PRIMARY_COLOR)
#         gradient.setColorAt(1, GameConfig.PRIMARY_COLOR.darker(150))
#         painter.setBrush(QBrush(gradient))
#         painter.setPen(Qt.PenStyle.NoPen)
#         if self.game.state_manager.state == GameState.GAME_OVER:
#             painter.drawEllipse(pacman_x, pacman_y, size, size)
#             painter.setOpacity(GameConfig.GLOW_OPACITY)
#             painter.setBrush(QBrush(text_color.lighter(150)))
#             painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#             painter.setOpacity(1.0)
#             painter.setBrush(QBrush(QColor(0, 0, 0)))
#             painter.drawEllipse(pacman_x + size // 4, pacman_y + size // 4, size // 4, size // 8)
#             painter.drawEllipse(pacman_x + size // 2, pacman_y + size // 4, size // 4, size // 8)
#             painter.setPen(QPen(text_color, 2))
#             for i in range(5):
#                 offset_y = int(20 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i))
#                 painter.drawLine(pacman_x + i * size // 5, pacman_y + size,
#                                  pacman_x + i * size // 5, pacman_y + size + offset_y)
#         else:
#             painter.drawPie(pacman_x, pacman_y, size, size, 30 * 16, 300 * 16)
#             painter.setOpacity(GameConfig.GLOW_OPACITY)
#             painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150)))
#             painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
#             painter.setOpacity(1.0)
#             eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(30)))
#             eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(30)))
#             painter.setBrush(QBrush(QColor(0, 0, 0)))
#             painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
#             painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR))
#             for i in range(8):
#                 angle = self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i * math.pi / 4
#                 spark_x = pacman_x + size // 2 + int(60 * math.cos(angle))
#                 spark_y = pacman_y + size // 2 + int(60 * math.sin(angle))
#                 painter.drawEllipse(spark_x - 3, spark_y - 3, 6, 6)
#         painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 2.5), QFont.Weight.Bold))
#         pulse = 1 + 0.15 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
#         for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#             painter.setPen(QPen(text_color.lighter(150), 2))
#             painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE + offset[0],
#                              height // 2 - 4 * GameConfig.CELL_SIZE + offset[1], text)
#         painter.setPen(QPen(text_color.lighter(100 + int(pulse * 50))))
#         painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE, height // 2 - 4 * GameConfig.CELL_SIZE, text)
#         painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height // 2 - GameConfig.CELL_SIZE,
#                                 24 * GameConfig.CELL_SIZE, 3 * GameConfig.CELL_SIZE, 10, 10)
#         painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
#         painter.setPen(QPen(QColor(255, 255, 255)))
#         opacity = 0.7 + 0.3 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
#         painter.setOpacity(opacity)
#         painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height // 2, f"Очки: {self.game.state_manager.score}")
#         painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, height // 2 + GameConfig.CELL_SIZE,
#                          "SPACE для рестарта | ESC для выхода")
#         painter.setOpacity(1.0)
#
#     def draw_pause_screen(self, painter, width, height):
#         """Отрисовывает экран паузы."""
#         self.draw_background(painter, width, height)
#         self.draw_map(painter)
#         for ghost in self.game.ghosts:
#             ghost.draw(painter)
#         self.draw_pacman(painter)
#         self.draw_hud(painter, width)
#         painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
#         painter.setPen(Qt.PenStyle.NoPen)
#         painter.drawRect(0, 0, width, height)
#         painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 2), QFont.Weight.Bold))
#         painter.setPen(QPen(QColor(255, 255, 255)))
#         painter.drawText(width // 2 - 6 * GameConfig.CELL_SIZE, height // 2, "ПАУЗА")
#         painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
#         painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height // 2 + 2 * GameConfig.CELL_SIZE,
#                          "Нажми P для продолжения")
#
# class PacmanGame(QWidget):
#     """Основной класс игры Pac-Man."""
#     def __init__(self):
#         super().__init__()
#         try:
#             self.setWindowTitle("Pac-Man")
#             self.state_manager = GameStateManager()
#             self.renderer = Renderer(self)
#             self.high_score_manager = HighScoreManager()
#             self.pacman_x = 14
#             self.pacman_y = 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.pacman_animation_frame = 0
#             self.screen_animation_frame = 0
#             self.ghosts = [
#                 Ghost(13.5, 11, QColor(255, 0, 0), 'Blinky'),
#                 Ghost(14.5, 11, QColor(255, 184, 255), 'Pinky'),
#                 Ghost(13.5, 13, QColor(0, 255, 255), 'Inky')
#             ]
#             self.original_map = [row[:] for row in MAP_DATA]
#             self.setup_ui()
#             self.setup_timer()
#             logging.info(f"Инициализация игры: Pac-Man на ({self.pacman_x}, {self.pacman_y}), призраков: {len(self.ghosts)}")
#         except Exception as e:
#             logging.error(f"Ошибка инициализации: {e}")
#             sys.exit(1)
#
#     def setup_ui(self):
#         """Настраивает пользовательский интерфейс и масштабирование."""
#         screen = QApplication.primaryScreen().geometry()
#         scale_factor = min(screen.width() / (GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE),
#                            screen.height() / (GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE))
#         GameConfig.CELL_SIZE = int(GameConfig.CELL_SIZE * scale_factor)
#         self.setFixedSize(screen.width(), screen.height())
#         self.offset_x = (screen.width() - GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE) // 2
#         self.offset_y = (screen.height() - GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE) // 2
#         self.showFullScreen()
#
#     def setup_timer(self):
#         """Настраивает игровой таймер."""
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.game_loop)
#         self.timer.setInterval(1000 // GameConfig.FPS)
#         self.timer.start()
#
#     def keyPressEvent(self, event):
#         """Обрабатывает нажатия клавиш."""
#         try:
#             key = event.key()
#             if self.state_manager.state == GameState.START:
#                 if key == Qt.Key.Key_Space:
#                     self.state_manager.state = GameState.PLAYING
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#             elif self.state_manager.state == GameState.PLAYING:
#                 if key in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
#                     self.next_direction = {
#                         Qt.Key.Key_Left: 'left',
#                         Qt.Key.Key_Right: 'right',
#                         Qt.Key.Key_Up: 'up',
#                         Qt.Key.Key_Down: 'down'
#                     }[key]
#                 elif key == Qt.Key.Key_P:
#                     self.state_manager.state = GameState.PAUSED
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#             elif self.state_manager.state == GameState.PAUSED:
#                 if key == Qt.Key.Key_P:
#                     self.state_manager.state = GameState.PLAYING
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#             elif self.state_manager.state in (GameState.GAME_OVER, GameState.WIN):
#                 if key == Qt.Key.Key_Space:
#                     self.reset_game()
#                 elif key == Qt.Key.Key_Escape:
#                     self.close()
#         except Exception as e:
#             logging.error(f"Ошибка обработки нажатия клавиши: {e}")
#
#     def can_move_to(self, x, y):
#         """Проверяет, можно ли переместиться в указанную клетку."""
#         try:
#             grid_x, grid_y = int(round(x)), int(round(y))
#             return (0 <= grid_x < GameConfig.MAP_WIDTH and
#                     0 <= grid_y < GameConfig.MAP_HEIGHT and
#                     MAP_DATA[grid_y][grid_x] != 1)
#         except Exception as e:
#             logging.error(f"Ошибка проверки движения: {e}")
#             return False
#
#     def move_pacman(self):
#         """Перемещает Pac-Man, учитывая возможность смены направления."""
#         try:
#             current_speed = GameConfig.PACMAN_BOOST_SPEED if self.state_manager.boost_timer > 0 else GameConfig.PACMAN_SPEED
#             if (abs(self.pacman_x - round(self.pacman_x)) < current_speed * 2 and
#                     abs(self.pacman_y - round(self.pacman_y)) < current_speed * 2):
#                 test_x, test_y = int(self.pacman_x), int(self.pacman_y)
#                 test_move_x, test_move_y = DIRECTIONS[self.next_direction]
#                 if self.can_move_to(test_x + test_move_x, test_y + test_move_y):
#                     self.pacman_direction = self.next_direction
#             dx, dy = DIRECTIONS[self.pacman_direction]
#             new_x, new_y = self.pacman_x + dx * current_speed, self.pacman_y + dy * current_speed
#             if self.can_move_to(new_x, new_y):
#                 self.pacman_x, self.pacman_y = new_x, new_y
#             else:
#                 self.pacman_x, self.pacman_y = round(self.pacman_x), round(self.pacman_y)
#             if self.pacman_x < -0.5:
#                 self.pacman_x = GameConfig.MAP_WIDTH - 0.5
#             elif self.pacman_x >= GameConfig.MAP_WIDTH + 0.5:
#                 self.pacman_x = -0.5
#             logging.debug(f"Pac-Man: позиция ({self.pacman_x:.2f}, {self.pacman_y:.2f}), направление {self.pacman_direction}")
#         except Exception as e:
#             logging.error(f"Ошибка движения Pac-Man: {e}")
#
#     def check_collisions(self):
#         """Проверяет столкновения Pac-Man с призраками."""
#         try:
#             for ghost in self.ghosts:
#                 # Увеличенный радиус для режима frightened
#                 collision_radius = 0.45 if ghost.behavior == 'frightened' else 0.35
#                 if abs(self.pacman_x - ghost.x) < collision_radius and abs(self.pacman_y - ghost.y) < collision_radius:
#                     if ghost.behavior == 'frightened':
#                         ghost.behavior = 'chase'
#                         ghost.x, ghost.y = ghost.home_x, ghost.home_y
#                         self.state_manager.score += 200
#                         # Визуальный эффект столкновения
#                         self.screen_animation_frame = 0  # Сброс для анимации
#                     else:
#                         self.state_manager.lives -= 1
#                         if self.state_manager.lives <= 0:
#                             self.state_manager.state = GameState.GAME_OVER
#                             self.high_score_manager.save_high_score(self.state_manager.score)
#                         else:
#                             self.reset_positions()
#         except Exception as e:
#             logging.error(f"Ошибка проверки столкновений: {e}")
#
#     def spawn_fruit(self):
#         """Спавнит фрукт в случайной доступной позиции."""
#         try:
#             if not self.state_manager.fruit_active and self.state_manager.pellets_eaten > 0 and self.state_manager.pellets_eaten % GameConfig.FRUIT_SPAWN_INTERVAL == 0:
#                 available = [(x, y) for y in range(GameConfig.MAP_HEIGHT) for x in range(GameConfig.MAP_WIDTH)
#                              if MAP_DATA[y][x] == 2 or MAP_DATA[y][x] == 0]
#                 if available:
#                     self.state_manager.fruit_x, self.state_manager.fruit_y = random.choice(available)
#                     self.state_manager.fruit_active = True
#                     logging.info(f"Фрукт появился на ({self.state_manager.fruit_x}, {self.state_manager.fruit_y})")
#         except Exception as e:
#             logging.error(f"Ошибка спавна фрукта: {e}")
#
#     def eat_dots(self):
#         """Обрабатывает поедание точек, силовых точек и фруктов."""
#         try:
#             x, y = int(self.pacman_x), int(self.pacman_y)
#             cell = MAP_DATA[y][x]
#             if cell == 2:
#                 MAP_DATA[y][x] = 0
#                 self.state_manager.score += 10
#                 self.state_manager.pellets_eaten += 1
#                 self.spawn_fruit()
#             elif cell == 3:
#                 MAP_DATA[y][x] = 0
#                 self.state_manager.score += 50
#                 self.state_manager.pellets_eaten += 1
#                 self.state_manager.boost_timer = GameConfig.BOOST_DURATION
#                 for ghost in self.ghosts:
#                     ghost.behavior = 'frightened'
#                     ghost.frightened_timer = GameConfig.MODE_DURATIONS['frightened'] * GameConfig.FPS
#                 self.spawn_fruit()
#             # Проверка фрукта
#             if self.state_manager.fruit_active and x == self.state_manager.fruit_x and y == self.state_manager.fruit_y:
#                 self.state_manager.fruit_active = False
#                 self.state_manager.score += GameConfig.FRUIT_SCORE
#                 logging.info(f"Фрукт съеден, +{GameConfig.FRUIT_SCORE} очков")
#             if self.state_manager.pellets_eaten >= GameConfig.TOTAL_PELLETS:
#                 self.state_manager.state = GameState.WIN
#                 self.state_manager.level += 1
#                 self.high_score_manager.save_high_score(self.state_manager.score)
#                 self.reset_positions()
#                 for y in range(GameConfig.MAP_HEIGHT):
#                     for x in range(GameConfig.MAP_WIDTH):
#                         MAP_DATA[y][x] = self.original_map[y][x]
#                 self.state_manager.pellets_eaten = 0
#                 for ghost in self.ghosts:
#                     ghost.speed = GameConfig.GHOST_SPEED * (1 + 0.1 * self.state_manager.level)
#         except Exception as e:
#             logging.error(f"Ошибка поедания точек: {e}")
#
#     def reset_positions(self):
#         """Сбрасывает позиции Pac-Man и призраков."""
#         try:
#             self.pacman_x, self.pacman_y = 14, 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.state_manager.boost_timer = 0
#             self.ghosts[0].x, self.ghosts[0].y = 13.5, 11
#             self.ghosts[1].x, self.ghosts[1].y = 14.5, 11
#             self.ghosts[2].x, self.ghosts[2].y = 13.5, 13
#             for ghost in self.ghosts:
#                 ghost.behavior = 'chase'
#                 ghost.path = []
#                 ghost.direction = 'right'
#                 ghost.target = ghost.scatter_targets[ghost.name]
#                 ghost.speed = GameConfig.GHOST_SPEED * (1 + 0.1 * self.state_manager.level)
#             logging.info(f"Сброс позиций: Pac-Man ({self.pacman_x}, {self.pacman_y}), призраки: {[g.name for g in self.ghosts]}")
#         except Exception as e:
#             logging.error(f"Ошибка сброса позиций: {e}")
#
#     def reset_game(self):
#         """Полностью сбрасывает игру."""
#         try:
#             self.state_manager.reset()
#             self.high_score_manager.save_high_score(self.state_manager.score)
#             self.pacman_x, self.pacman_y = 14, 23
#             self.pacman_direction = 'right'
#             self.next_direction = 'right'
#             self.ghosts = [
#                 Ghost(13.5, 11, QColor(255, 0, 0), 'Blinky'),
#                 Ghost(14.5, 11, QColor(255, 184, 255), 'Pinky'),
#                 Ghost(13.5, 13, QColor(0, 255, 255), 'Inky')
#             ]
#             for y in range(GameConfig.MAP_HEIGHT):
#                 for x in range(GameConfig.MAP_WIDTH):
#                     MAP_DATA[y][x] = self.original_map[y][x]
#             self.pacman_animation_frame = 0
#             self.screen_animation_frame = 0
#             logging.info("Полный сброс игры")
#         except Exception as e:
#             logging.error(f"Ошибка сброса игры: {e}")
#
#     def game_loop(self):
#         """Основной игровой цикл."""
#         try:
#             if self.state_manager.state == GameState.PLAYING:
#                 self.move_pacman()
#                 self.eat_dots()
#                 if self.state_manager.boost_timer > 0:
#                     self.state_manager.boost_timer -= 1
#                 blinky_x, blinky_y = self.ghosts[0].x, self.ghosts[0].y
#                 for ghost in self.ghosts:
#                     ghost.update(self.pacman_x, self.pacman_y, self.pacman_direction, self.next_direction, blinky_x, blinky_y)
#                 self.check_collisions()
#                 self.state_manager.switch_mode()
#                 for ghost in self.ghosts:
#                     if ghost.behavior != 'frightened':
#                         ghost.behavior = self.state_manager.mode
#             self.pacman_animation_frame = (self.pacman_animation_frame + 1) % 20
#             self.screen_animation_frame = (self.screen_animation_frame + 1) % 60
#             self.update()
#         except Exception as e:
#             logging.error(f"Ошибка игрового цикла: {e}")
#
#     def paintEvent(self, event):
#         """Отрисовывает игру в зависимости от состояния."""
#         try:
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#             width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
#             height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
#             painter.translate(self.offset_x, self.offset_y)
#
#             if self.state_manager.state == GameState.START:
#                 self.renderer.draw_start_screen(painter, width, height)
#             elif self.state_manager.state == GameState.PLAYING:
#                 self.renderer.draw_background(painter, width, height)
#                 self.renderer.draw_map(painter)
#                 for ghost in self.ghosts:
#                     ghost.draw(painter)
#                 self.renderer.draw_pacman(painter)
#                 self.renderer.draw_hud(painter, width)
#             elif self.state_manager.state == GameState.PAUSED:
#                 self.renderer.draw_pause_screen(painter, width, height)
#             elif self.state_manager.state in (GameState.GAME_OVER, GameState.WIN):
#                 self.renderer.draw_game_over_win(painter, width, height)
#         except Exception as e:
#             logging.error(f"Ошибка отрисовки: {e}")
#
# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         game = PacmanGame()
#         sys.exit(app.exec())
#     except Exception as e:
#         logging.error(f"Ошибка приложения: {e}")
#         print(f"Не удалось запустить игру: {e}")
#         sys.exit(1)
#
#
#         sys.exit(1)
#
#
#














import sys
import random
import math
import os
import logging
import time
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPolygon, QBrush, QPainterPath, QRadialGradient, QLinearGradient
from PyQt6.QtCore import QPoint, Qt, QTimer, QCoreApplication, QRectF
from heapq import heappush, heappop
from enum import Enum

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Исправление путей для PyQt6 плагинов
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    os.path.dirname(QCoreApplication.applicationFilePath()), 'Qt', 'plugins'
)

# === Конфигурация ===

class GameState(Enum):
    """Состояния игры."""
    START = "start"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WIN = "win"

class GameConfig:
    """Константы игры."""
    CELL_SIZE = 20
    MAP_WIDTH = 28
    MAP_HEIGHT = 31
    FPS = 60
    GHOST_SPEED = 0.2
    PACMAN_SPEED = 0.2
    PACMAN_BOOST_SPEED = 0.24
    PACMAN_DASH_SPEED = 0.4
    PACMAN_SUPER_SPEED = 0.4
    MODE_DURATIONS = {'scatter': 7, 'chase': 20, 'frightened': 10}
    TOTAL_PELLETS = 250
    FONT = "Arial"
    PRIMARY_COLOR = QColor(255, 255, 0)
    SECONDARY_COLOR = QColor(20, 20, 80)
    WALL_COLOR = QColor(0, 0, 240)
    PELLET_COLOR = QColor(255, 255, 200)
    POWER_PELLET_COLOR = QColor(255, 200, 100)
    FRUIT_COLOR = QColor(255, 0, 0)
    SHIELD_COLOR = QColor(0, 200, 255)
    GLOW_OPACITY = 0.4
    ANIMATION_SPEED = 0.2
    HIGH_SCORE_FILE = "highscore.txt"
    FRUIT_SCORE = 100
    BOOST_DURATION = 6 * FPS
    DASH_COOLDOWN = 5 * FPS
    SUPER_DURATION = 8 * FPS
    SHIELD_DURATION = 2 * FPS
    FRUIT_SPAWN_INTERVAL = 50
    SECRET_FRUIT_BONUS = 500
    MAX_FRUITS_PER_LEVEL = 5
    ENABLE_EFFECTS = True  # Отключить для слабых машин

# Карта с телепортами (4)
MAP_DATA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,2,0,0,2,1,1,1,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,2,0,0,2,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,4,1,1,1,2,1,1,0,1,0,2,0,0,2,0,1,0,1,1,2,1,1,1,4,1,1],
    [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,2,0,0,2,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,2,0,0,2,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

DIRECTIONS = {
    'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)
}

# === Игровые объекты ===

class Star:
    """Фоновая звезда."""
    def __init__(self, x, y, brightness, speed, size):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.speed = speed
        self.size = size

    def update(self):
        self.brightness += self.speed
        if self.brightness > 255:
            self.brightness = 255
            self.speed = -self.speed
        elif self.brightness < 50:
            self.brightness = 50
            self.speed = -self.speed

class Particle:
    """Частица для эффектов."""
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1

    def draw(self, painter, offset_x, offset_y):
        size = GameConfig.CELL_SIZE * (1 - self.age / self.lifetime) * 0.2
        painter.setOpacity(1 - self.age / self.lifetime)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(self.x + offset_x - size / 2), int(self.y + offset_y - size / 2), int(size), int(size))
        painter.setOpacity(1.0)

class Ghost:
    """Класс призрака."""
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.behavior = 'chase'
        self.direction = 'right'
        self.frightened_timer = 0
        self.home_x = x
        self.home_y = y
        self.speed = GameConfig.GHOST_SPEED
        self.scatter_targets = {
            'Blinky': (26, 1), 'Pinky': (1, 1), 'Inky': (26, 29)
        }
        self.target = self.scatter_targets[name]
        self.path = []
        self.last_path = []
        self.path_timer = 0
        logging.info(f"Инициализация призрака {self.name} на позиции ({self.x}, {self.y})")

    def can_move_to(self, x, y):
        grid_x, grid_y = int(round(x)), int(round(y))
        return (0 <= grid_x < GameConfig.MAP_WIDTH and
                0 <= grid_y < GameConfig.MAP_HEIGHT and
                MAP_DATA[grid_y][grid_x] not in (1, 4))

    def get_available_directions(self):
        return [d for d, (dx, dy) in DIRECTIONS.items() if self.can_move_to(self.x + dx, self.y + dy)]

    def is_in_corridor(self, pacman_x, pacman_y):
        x, y = int(pacman_x), int(pacman_y)
        exits = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GameConfig.MAP_WIDTH and 0 <= ny < GameConfig.MAP_HEIGHT and MAP_DATA[ny][nx] not in (1, 4):
                exits += 1
        return exits <= 2

    def a_star(self, start_x, start_y, target_x, target_y, avoid_dead_ends=True):
        start_x, start_y = int(round(start_x)), int(round(start_y))
        target_x, target_y = int(round(target_x)), int(round(target_y))
        open_set = [(0, start_x, start_y, [])]
        closed_set = set()
        g_score = {(start_x, start_y): 0}
        f_score = {(start_x, start_y): abs(target_x - start_x) + abs(target_y - start_y)}
        max_nodes = 300
        start_time = time.time()
        time_limit = 0.01

        while open_set and len(open_set) < max_nodes and time.time() - start_time < time_limit:
            _, x, y, path = heappop(open_set)
            if (x, y) == (target_x, target_y):
                self.last_path = path
                return path
            if (x, y) in closed_set:
                continue
            closed_set.add((x, y))
            for direction, (dx, dy) in DIRECTIONS.items():
                next_x, next_y = x + dx, y + dy
                if not self.can_move_to(next_x, next_y):
                    continue
                if avoid_dead_ends:
                    available_dirs = sum(1 for d, (ndx, ndy) in DIRECTIONS.items()
                                        if self.can_move_to(next_x + ndx, next_y + ndy))
                    if available_dirs <= 1 and (next_x, next_y) != (target_x, target_y):
                        continue
                tentative_g_score = g_score[(x, y)] + 1
                if (next_x, next_y) not in g_score or tentative_g_score < g_score[(next_x, next_y)]:
                    g_score[(next_x, next_y)] = tentative_g_score
                    f_score[(next_x, next_y)] = tentative_g_score + abs(target_x - next_x) + abs(target_y - next_y)
                    heappush(open_set, (f_score[(next_x, next_y)], next_x, next_y, path + [direction]))
        logging.warning(f"Путь для {self.name} не найден, возвращаю последний путь")
        return self.last_path if self.last_path else []

    def get_target(self, pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y, level, dash_active):
        if self.behavior == 'scatter':
            return self.scatter_targets[self.name]
        elif self.behavior == 'frightened' and random.random() > 0.1 * min(level, 3):
            teleport_positions = [(1, 15), (26, 15)]
            if self.name == 'Inky':
                distances = [(abs(self.x - tx) + abs(self.y - ty), (tx, ty)) for tx, ty in teleport_positions]
                return min(distances)[1] if distances else (self.x, self.y)
            available = [(x, y) for x in range(GameConfig.MAP_WIDTH) for y in range(GameConfig.MAP_HEIGHT)
                         if MAP_DATA[y][x] not in (1, 4)]
            return random.choice(available)
        else:
            trap_mode = self.is_in_corridor(pacman_x, pacman_y) and random.random() < 0.5 and self.name == 'Blinky'
            if trap_mode:
                exits = [(pacman_x + dx, pacman_y + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                         if self.can_move_to(pacman_x + dx, pacman_y + dy)]
                return random.choice(exits) if exits else (pacman_x, pacman_y)
            if self.name == 'Blinky':
                if random.random() < 0.3:
                    dx, dy = DIRECTIONS.get(pacman_direction, (0, 0))
                    return (max(0, min(GameConfig.MAP_WIDTH - 1, pacman_x + dx)), pacman_y + dy)
                return (pacman_x, pacman_y)
            elif self.name == 'Pinky':
                distance = 8 if dash_active else 6
                dx, dy = DIRECTIONS.get(next_direction, DIRECTIONS[pacman_direction])
                target_x = max(0, min(GameConfig.MAP_WIDTH - 1, pacman_x + dx * distance))
                target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, pacman_y + dy * distance))
                if random.random() < 0.2:
                    available = [(x, y) for x in range(GameConfig.MAP_WIDTH) for y in range(GameConfig.MAP_HEIGHT)
                                 if MAP_DATA[y][x] not in (1, 4) and abs(x - pacman_x) + abs(y - pacman_y) < 10]
                    return random.choice(available) if available else (target_x, target_y)
                return (target_x, target_y)
            else:  # Inky
                dx, dy = DIRECTIONS.get(next_direction, DIRECTIONS[pacman_direction])
                intermediate_x = pacman_x + dx * 2
                intermediate_y = pacman_y + dy * 2
                target_x = max(0, min(GameConfig.MAP_WIDTH - 1, blinky_x + 2 * (intermediate_x - blinky_x)))
                target_y = max(0, min(GameConfig.MAP_HEIGHT - 1, blinky_y + 2 * (intermediate_y - blinky_y)))
                if random.random() < 0.25 and abs(blinky_x - pacman_x) + abs(blinky_y - pacman_y) > 10:
                    available = [(x, y) for x in range(GameConfig.MAP_WIDTH) for y in range(GameConfig.MAP_HEIGHT)
                                 if MAP_DATA[y][x] not in (1, 4) and abs(x - pacman_x) + abs(y - pacman_y) < 5]
                    return random.choice(available) if available else (target_x, target_y)
                return (target_x, target_y)

    def check_collision_with_ghosts(self, ghosts):
        for other in ghosts:
            if other != self and abs(self.x - other.x) < 0.5 and abs(self.y - other.y) < 0.5:
                available = self.get_available_directions()
                if available:
                    self.direction = random.choice(available)
                    self.path = []
                    logging.info(f"Антиколлизия: {self.name} меняет направление на {self.direction}")
                return True
        return False

    def update(self, pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y, level, ghosts, dash_active):
        try:
            speed = self.speed * (1.1 if self.behavior == 'chase' and level >= 2 else 1.0)
            if self.behavior == 'frightened':
                self.frightened_timer -= 1
                if self.frightened_timer <= 0:
                    self.behavior = 'chase'
            self.path_timer -= 1
            if abs(self.x - round(self.x)) < 0.01 and abs(self.y - round(self.y)) < 0.01:
                if self.check_collision_with_ghosts(ghosts):
                    return
                if self.path_timer <= 0:
                    self.target = self.get_target(pacman_x, pacman_y, pacman_direction, next_direction, blinky_x, blinky_y, level, dash_active)
                    self.path = self.a_star(self.x, self.y, self.target[0], self.target[1], avoid_dead_ends=self.name != 'Blinky' or level < 3)
                    self.path_timer = 5
                if self.path:
                    self.direction = self.path.pop(0)
                else:
                    available = self.get_available_directions()
                    if available:
                        self.direction = random.choice([d for d in available if d != {
                            'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'
                        }.get(self.direction, d)]) or random.choice(available)
                        logging.warning(f"Призрак {self.name} выбирает случайное направление {self.direction} на ({self.x}, {self.y})")
            dx, dy = DIRECTIONS[self.direction]
            new_x, new_y = self.x + dx * speed, self.y + dy * speed
            if self.can_move_to(new_x, new_y):
                self.x, self.y = new_x, new_y

            else:
                self.x, self.y = round(self.x), round(self.y)
                available = self.get_available_directions()
                if available:
                    self.direction = random.choice(available)
                    self.path = []
                    logging.warning(f"Призрак {self.name} застрял на ({self.x}, {self.y}), новое направление {self.direction}")
                else:
                    logging.error(f"Призрак {self.name} полностью застрял на ({self.x}, {self.y})")
            if self.x < -0.5:
                self.x = GameConfig.MAP_WIDTH - 0.5
            elif self.x >= GameConfig.MAP_WIDTH + 0.5:
                self.x = -0.5
            teleport_positions = [(1, 15), (26, 15)]
            for tx, ty in teleport_positions:
                if abs(self.x - tx) < 0.5 and abs(self.y - ty) < 0.5:
                    other_tx, other_ty = teleport_positions[1 - teleport_positions.index((tx, ty))]
                    self.x, self.y = other_tx, other_ty
                    self.path = []
                    logging.info(f"Телепортация призрака {self.name} с ({tx}, {ty}) на ({other_tx}, {other_ty})")
                    break
            logging.debug(f"Призрак {self.name}: позиция ({self.x:.2f}, {self.y:.2f}), направление {self.direction}")
        except Exception as e:
            logging.error(f"Ошибка обновления призрака {self.name}: {e}")

    def draw(self, painter, offset_x, offset_y):
        try:
            if not GameConfig.ENABLE_EFFECTS:
                painter.setBrush(QBrush(self.color))
                painter.setPen(Qt.PenStyle.NoPen)
                size = GameConfig.CELL_SIZE
                x = int(self.x * size + offset_x)
                y = int(self.y * size + offset_y)
                painter.drawEllipse(x, y, size, size)
                return
            size = GameConfig.CELL_SIZE
            x = int(self.x * size + offset_x)
            y = int(self.y * size + offset_y)
            gradient = QLinearGradient(x, y, x, y + size)
            if self.behavior == 'frightened':
                gradient.setColorAt(0, QColor(0, 0, 255))
                gradient.setColorAt(1, QColor(0, 0, 180))
            else:
                gradient.setColorAt(0, self.color.lighter(130))
                gradient.setColorAt(1, self.color.darker(130))
            painter.setBrush(QBrush(gradient))
            path = QPainterPath()
            path.addEllipse(x, y, size, size * 0.8)
            path.addRect(x, y + size * 0.4, size, size * 0.6)
            painter.drawPath(path)
            points = [
                QPoint(x, y + size),
                QPoint(x + size // 4, y + size - size // 8),
                QPoint(x + size // 2, y + size),
                QPoint(x + 3 * size // 4, y + size - size // 8),
                QPoint(x + size, y + size)
            ]
            painter.setPen(QPen(self.color.darker(150), 2))
            painter.drawPolyline(QPolygon(points))
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            eye_dir = {'up': (0, -0.05), 'down': (0, 0.05), 'left': (-0.05, 0), 'right': (0.05, 0)}[self.direction]
            for offset in [(0.3, 0.2), (0.5, 0.2)]:
                white_eye_x = int(x + size * offset[0])
                white_eye_y = int(y + size * offset[1])
                painter.drawEllipse(white_eye_x, white_eye_y, int(size * 0.2), int(size * 0.2))
                eye_x = int(x + size * (offset[0] + 0.05 + eye_dir[0]))
                eye_y = int(y + size * (offset[1] + 0.05 + eye_dir[1]))
                painter.setBrush(QBrush(QColor(0, 0, 255)))
                painter.drawEllipse(eye_x, eye_y, int(size * 0.1), int(size * 0.1))
            painter.setOpacity(GameConfig.GLOW_OPACITY)
            painter.setBrush(QBrush(self.color.lighter(150)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x - size * 0.1, y - size * 0.1, size * 1.2, size * 1.2)
            painter.setOpacity(1.0)
        except Exception as e:
            logging.error(f"Ошибка отрисовки призрака {self.name}: {e}")

# === Управление состоянием ===

class HighScoreManager:
    """Управление рекордами."""
    def __init__(self):
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open(GameConfig.HIGH_SCORE_FILE, 'r') as f:
                return int(f.read() or 0)
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(GameConfig.HIGH_SCORE_FILE, 'w') as f:
                    f.write(str(score))
            except Exception as e:
                logging.error(f"Ошибка сохранения рекорда: {e}")

class GameStateManager:
    """Управление состоянием игры."""
    def __init__(self):
        self.state = GameState.START
        self.mode = 'scatter'
        self.mode_timer = 0
        self.score = 0
        self.lives = 3
        self.pellets_eaten = 0
        self.level = 1
        self.fruit_active = False
        self.fruit_x = 0
        self.fruit_y = 0
        self.fruits_collected = 0
        self.boost_timer = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.super_timer = 0
        self.power_pellets_eaten = 0
        self.shield_active = False
        self.shield_available = True
        self.sticky_timer = 0

    def switch_mode(self):
        self.mode_timer += 1
        if self.mode_timer >= GameConfig.MODE_DURATIONS[self.mode] * GameConfig.FPS:
            self.mode_timer = 0
            self.mode = 'chase' if self.mode == 'scatter' else 'scatter'

    def reset(self):
        self.state = GameState.PLAYING
        self.mode = 'scatter'
        self.mode_timer = 0
        self.score = 0
        self.lives = 3
        self.pellets_eaten = 0
        self.level = 1
        self.fruit_active = False
        self.fruits_collected = 0
        self.boost_timer = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.super_timer = 0
        self.power_pellets_eaten = 0
        self.shield_active = False
        self.shield_available = True
        self.sticky_timer = 0

# === Отрисовка ===

class Renderer:
    """Отрисовка игры."""
    def __init__(self, game):
        self.game = game
        width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
        height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
        self.stars = [Star(random.randint(0, width - 1),
                          random.randint(0, height - 1),
                          random.randint(50, 255),
                          random.uniform(0.2, 0.8) * random.choice([-1, 1]),
                          random.randint(4, 8)) for _ in range(50)] if GameConfig.ENABLE_EFFECTS else []
        self.wall_gradient = QLinearGradient(0, 0, 0, GameConfig.CELL_SIZE)
        self.wall_gradient.setColorAt(0, GameConfig.WALL_COLOR.lighter(130))
        self.wall_gradient.setColorAt(1, GameConfig.WALL_COLOR.darker(130))
        self.bg_gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
        self.bg_gradient.setColorAt(0, GameConfig.SECONDARY_COLOR)
        self.bg_gradient.setColorAt(1, QColor(0, 0, 0))
        self.pacman_gradient = QRadialGradient(0, 0, GameConfig.CELL_SIZE)
        self.pacman_gradient.setColorAt(0, GameConfig.PRIMARY_COLOR)
        self.pacman_gradient.setColorAt(1, GameConfig.PRIMARY_COLOR.darker(150))
        self.transition_timer = 0
        self.transition_particles = []

    def start_level_transition(self):
        if not GameConfig.ENABLE_EFFECTS:
            return
        self.transition_timer = GameConfig.FPS
        width = GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE
        height = GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE
        self.transition_particles = [
            Particle(
                random.randint(0, width),
                random.randint(0, height),
                random.uniform(-2, 2),
                random.uniform(-2, 2),
                GameConfig.PRIMARY_COLOR.lighter(150),
                60
            ) for _ in range(20)
        ]

    def draw_background(self, painter, width, height):
        painter.fillRect(0, 0, width, height, QBrush(self.bg_gradient))
        if not GameConfig.ENABLE_EFFECTS:
            return
        for star in self.stars:
            star.update()
            painter.setOpacity(star.brightness / 255)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(star.x, star.y, star.size, star.size)
        painter.setOpacity(1.0)

    def draw_map(self, painter, offset_x, offset_y):
        for y in range(GameConfig.MAP_HEIGHT):
            for x in range(GameConfig.MAP_WIDTH):
                cell = MAP_DATA[y][x]
                rect_x, rect_y = x * GameConfig.CELL_SIZE + offset_x, y * GameConfig.CELL_SIZE + offset_y
                if cell in (1, 4):
                    painter.setBrush(QBrush(self.wall_gradient))
                    painter.setPen(QPen(GameConfig.WALL_COLOR, 2))
                    path = QPainterPath()
                    path.addRoundedRect(QRectF(rect_x, rect_y, GameConfig.CELL_SIZE, GameConfig.CELL_SIZE), 5, 5)
                    painter.drawPath(path)
                    if GameConfig.ENABLE_EFFECTS:
                        painter.setOpacity(GameConfig.GLOW_OPACITY)
                        painter.setBrush(QBrush(GameConfig.WALL_COLOR.lighter(150)))
                        painter.drawRoundedRect(QRectF(rect_x - 2, rect_y - 2, GameConfig.CELL_SIZE + 4, GameConfig.CELL_SIZE + 4), 5, 5)
                        painter.setOpacity(1.0)
                elif cell == 2:
                    painter.setBrush(QBrush(GameConfig.PELLET_COLOR))
                    painter.setPen(Qt.PenStyle.NoPen)
                    center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
                    painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)
                elif cell == 3:
                    pulse = 8 + 3 * math.sin(self.game.pacman_animation_frame * GameConfig.ANIMATION_SPEED * 1.5)
                    painter.setBrush(QBrush(GameConfig.POWER_PELLET_COLOR))
                    painter.setPen(Qt.PenStyle.NoPen)
                    center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
                    size = int(pulse * 2)
                    painter.drawEllipse(center_x - size // 2, center_y - size // 2, size, size)
                    if GameConfig.ENABLE_EFFECTS:
                        painter.setOpacity(GameConfig.GLOW_OPACITY * (0.5 + 0.5 * math.sin(self.game.pacman_animation_frame * GameConfig.ANIMATION_SPEED)))
                        painter.setBrush(QBrush(GameConfig.POWER_PELLET_COLOR.lighter(150)))
                        painter.drawEllipse(center_x - size, center_y - size, size * 2, size * 2)
                        painter.setOpacity(1.0)
                elif cell == 5:
                    painter.setBrush(QBrush(QColor(100, 100, 100, 100)))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(rect_x, rect_y, GameConfig.CELL_SIZE, GameConfig.CELL_SIZE)
        if self.game.state_manager.fruit_active:
            fruit_x, fruit_y = self.game.state_manager.fruit_x, self.game.state_manager.fruit_y
            rect_x, rect_y = fruit_x * GameConfig.CELL_SIZE + offset_x, fruit_y * GameConfig.CELL_SIZE + offset_y
            painter.setBrush(QBrush(GameConfig.FRUIT_COLOR))
            painter.setPen(Qt.PenStyle.NoPen)
            center_x, center_y = rect_x + GameConfig.CELL_SIZE // 2, rect_y + GameConfig.CELL_SIZE // 2
            painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)
            if GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(GameConfig.FRUIT_COLOR.lighter(150)))
                painter.drawEllipse(center_x - 7, center_y - 7, 14, 14)
                painter.setOpacity(1.0)

    def draw_pacman(self, painter, offset_x, offset_y, camera_scale):
        try:
            if not GameConfig.ENABLE_EFFECTS:
                painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR))
                painter.setPen(Qt.PenStyle.NoPen)
                size = GameConfig.CELL_SIZE * camera_scale
                x = int(self.game.pacman_x * GameConfig.CELL_SIZE * camera_scale + offset_x)
                y = int(self.game.pacman_y * GameConfig.CELL_SIZE * camera_scale + offset_y)
                painter.drawEllipse(x, y, size, size)
                return
            size = GameConfig.CELL_SIZE * camera_scale
            crunch = 1 + 0.05 * math.sin(self.game.pacman_animation_frame * GameConfig.ANIMATION_SPEED * 2)
            x = int(self.game.pacman_x * GameConfig.CELL_SIZE * camera_scale + offset_x)
            y = int(self.game.pacman_y * GameConfig.CELL_SIZE * camera_scale + offset_y)
            painter.setBrush(QBrush(self.pacman_gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            start_angle = {'right': 30, 'left': 210, 'up': 300, 'down': 120}.get(self.game.pacman_direction, 30) * 16
            if self.game.sad_timer > 0:
                start_angle = (start_angle // 16 + 180) % 360 * 16
            span_angle = {
                0: 360 * 16, 1: 330 * 16, 2: 300 * 16, 3: 330 * 16
            }.get(self.game.pacman_animation_frame % 4, 360 * 16)
            painter.drawPie(x, y, int(size * crunch), int(size * crunch), start_angle, span_angle)
            if self.game.state_manager.super_timer > 0 and GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(QColor(255, 215, 0)))
                painter.drawEllipse(x - size * 0.2, y - size * 0.2, size * 1.4, size * 1.4)
                for angle in range(0, 360, 45):
                    wave_x = x + size // 2 + int(20 * math.cos(math.radians(angle + self.game.pacman_animation_frame * 5)))
                    wave_y = y + size // 2 + int(20 * math.sin(math.radians(angle + self.game.pacman_animation_frame * 5)))
                    painter.drawEllipse(wave_x - 5, wave_y - 5, 10, 10)
                painter.setOpacity(1.0)
            elif self.game.state_manager.boost_timer > 0 and GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(200)))
                painter.drawEllipse(x - size * 0.2, y - size * 0.2, size * 1.4, size * 1.4)
                for angle in range(0, 360, 90):
                    wave_x = x + size // 2 + int(15 * math.cos(math.radians(angle + self.game.pacman_animation_frame * 3)))
                    wave_y = y + size // 2 + int(15 * math.sin(math.radians(angle + self.game.pacman_animation_frame * 3)))
                    painter.drawEllipse(wave_x - 3, wave_y - 3, 6, 6)
                painter.setOpacity(1.0)
            elif GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150)))
                painter.drawEllipse(x - size * 0.1, y - size * 0.1, size * 1.2, size * 1.2)
                painter.setOpacity(1.0)
            if self.game.state_manager.shield_active and GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(0.7)
                painter.setBrush(QBrush(GameConfig.SHIELD_COLOR))
                painter.drawEllipse(x - size * 0.15, y - size * 0.15, size * 1.3, size * 1.3)
                painter.setOpacity(1.0)
            eye_x = x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
            eye_y = y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
            for particle in self.game.particles:
                particle.draw(painter, offset_x, offset_y)
        except Exception as e:
            logging.error(f"Ошибка отрисовки Pac-Man: {e}")

    def draw_hud(self, painter, width):
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, width, int(GameConfig.CELL_SIZE * 1.5))
        painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE // 2))
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(10, GameConfig.CELL_SIZE, f"Очки: {self.game.state_manager.score}")
        painter.drawText(width - 20 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE,
                         f"Жизни: {self.game.state_manager.lives} | Уровень: {self.game.state_manager.level} | Рекорд: {self.game.high_score_manager.high_score}")
        painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE,
                         f"FPS: {self.game.current_fps:.1f} | Фрукты: {self.game.state_manager.fruits_collected}/{GameConfig.MAX_FRUITS_PER_LEVEL}")
        if self.game.state_manager.boost_timer > 0:
            painter.setPen(QPen(QColor(255, 255, 0)))
            painter.drawText(width // 2 - 5 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE, "Ускорение!")
        if self.game.state_manager.super_timer > 0:
            painter.setPen(QPen(QColor(255, 215, 0)))
            painter.drawText(width // 2 - 5 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE, "Суперрежим!")
        if self.game.state_manager.dash_cooldown > 0:
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(width // 2 + 5 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE,
                             f"Рывок: {self.game.state_manager.dash_cooldown // GameConfig.FPS + 1}с")
        if self.game.state_manager.shield_available and not self.game.state_manager.shield_active:
            painter.setPen(QPen(GameConfig.SHIELD_COLOR))
            painter.drawText(width // 2 + 10 * GameConfig.CELL_SIZE, GameConfig.CELL_SIZE, "Щит: S")

    def draw_start_screen(self, painter, width, height):
        self.draw_background(painter, width, height)
        pulse = 1 + 0.15 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
        painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 3.5 * pulse), QFont.Weight.Bold))
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            painter.setPen(QPen(GameConfig.PRIMARY_COLOR.lighter(150), 2))
            painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE + offset[0],
                             height // 2 - 3 * GameConfig.CELL_SIZE + offset[1], "Pac-Man")
        painter.setPen(QPen(GameConfig.PRIMARY_COLOR))
        painter.drawText(width // 2 - 9 * GameConfig.CELL_SIZE, height // 2 - 3 * GameConfig.CELL_SIZE, "Pac-Man")
        size = GameConfig.CELL_SIZE * 3
        pacman_x = width // 2 - size // 2 + int(50 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED))
        pacman_y = height // 2
        painter.setBrush(QBrush(self.pacman_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        start_angle = 30 * 16
        span_angle = {
            0: 360 * 16, 1: 330 * 16, 2: 300 * 16, 3: 330 * 16
        }.get(self.game.pacman_animation_frame % 4, 360 * 16)
        painter.drawPie(pacman_x, pacman_y, size, size, start_angle, span_angle)
        if GameConfig.ENABLE_EFFECTS:
            painter.setOpacity(GameConfig.GLOW_OPACITY)
            painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150)))
            painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
            painter.setOpacity(1.0)
        eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(start_angle / 16)))
        eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(start_angle / 16)))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
        for i, ghost in enumerate(self.game.ghosts):
            ghost_x = width // 2 + int(100 * math.cos(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i * math.pi / 2)) - size // 2
            ghost_y = height // 2 + int(50 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i * math.pi / 2)) - size // 2
            gradient = QLinearGradient(ghost_x, ghost_y, ghost_x, ghost_y + size)
            gradient.setColorAt(0, ghost.color.lighter(130))
            gradient.setColorAt(1, ghost.color.darker(130))
            painter.setBrush(QBrush(gradient))
            path = QPainterPath()
            path.addEllipse(ghost_x, ghost_y, size, size * 0.8)
            path.addRect(ghost_x, ghost_y + size * 0.4, size, size * 0.6)
            painter.drawPath(path)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height - 3 * GameConfig.CELL_SIZE,
                                24 * GameConfig.CELL_SIZE, 2 * GameConfig.CELL_SIZE, 10, 10)
        painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
        painter.setPen(QPen(QColor(255, 255, 255)))
        opacity = 0.7 + 0.3 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
        painter.setOpacity(opacity)
        painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height - 2 * GameConfig.CELL_SIZE,
                         "Нажми SPACE для старта")
        painter.drawText(width // 2 - 12 * GameConfig.CELL_SIZE, height - GameConfig.CELL_SIZE,
                         "Стрелки: Двигаться | Двойное нажатие: Рывок | S: Щит | P: Пауза | ESC: Выход")
        painter.setOpacity(1.0)

    def draw_game_over_win(self, painter, width, height):
        star_color = QColor(255, 255, 255)
        text = "ПОБЕДА!" if self.game.state_manager.state == GameState.WIN else "ИГРА ОКОНЧЕНА"
        text_color = QColor(0, 255, 0) if self.game.state_manager.state == GameState.WIN else QColor(255, 0, 0)
        gradient = QRadialGradient(width // 2, height // 2, max(width, height) // 2)
        gradient.setColorAt(0, text_color.darker(150))
        gradient.setColorAt(1, QColor(0, 0, 0))
        star_color = text_color
        painter.fillRect(0, 0, width, height, QBrush(gradient))
        if GameConfig.ENABLE_EFFECTS:
            for star in self.stars:
                painter.setOpacity(star.brightness / 255)
                painter.setBrush(QBrush(star_color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(star.x, star.y, star.size, star.size)
            painter.setOpacity(1.0)
        size = GameConfig.CELL_SIZE * 4
        pacman_x = width // 2 - size // 2
        pacman_y = height // 2 - size + int(20 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED))
        painter.setBrush(QBrush(self.pacman_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        if self.game.state_manager.state == GameState.GAME_OVER:
            painter.drawEllipse(pacman_x, pacman_y, size, size)
            if GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(text_color.lighter(150)))
                painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
                painter.setOpacity(1.0)
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawEllipse(pacman_x + size // 4, pacman_y + size // 4, size // 4, size // 8)
            painter.drawEllipse(pacman_x + size // 2, pacman_y + size // 4, size // 4, size // 8)
            painter.setPen(QPen(text_color, 2))
            for i in range(5):
                offset_y = int(20 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i))
                painter.drawLine(pacman_x + i * size // 5, pacman_y + size,
                                 pacman_x + i * size // 5, pacman_y + size + offset_y)
        else:
            painter.drawPie(pacman_x, pacman_y, size, size, 30 * 16, 300 * 16)
            if GameConfig.ENABLE_EFFECTS:
                painter.setOpacity(GameConfig.GLOW_OPACITY)
                painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR.lighter(150)))
                painter.drawEllipse(pacman_x - size * 0.2, pacman_y - size * 0.2, size * 1.4, size * 1.4)
                painter.setOpacity(1.0)
            eye_x = pacman_x + size * (0.5 + 0.2 * math.cos(math.radians(30)))
            eye_y = pacman_y + size * (0.5 - 0.2 * math.sin(math.radians(30)))
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawEllipse(int(eye_x - size * 0.1), int(eye_y - size * 0.1), int(size * 0.2), int(size * 0.2))
            if GameConfig.ENABLE_EFFECTS:
                painter.setBrush(QBrush(GameConfig.PRIMARY_COLOR))
                for i in range(8):
                    angle = self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED + i * math.pi / 4
                    spark_x = pacman_x + size // 2 + int(60 * math.cos(angle))
                    spark_y = pacman_y + size // 2 + int(60 * math.sin(angle))
                    painter.drawEllipse(spark_x - 3, spark_y - 3, 6, 6)
        painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 2.5), QFont.Weight.Bold))
        pulse = 1 + 0.15 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            painter.setPen(QPen(text_color.lighter(150), 2))
            painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE + offset[0],
                             height // 2 - 4 * GameConfig.CELL_SIZE + offset[1], text)
        painter.setPen(QPen(text_color.lighter(100 + int(pulse * 50))))
        painter.drawText(width // 2 - 11 * GameConfig.CELL_SIZE, height // 2 - 4 * GameConfig.CELL_SIZE, text)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(width // 2 - 12 * GameConfig.CELL_SIZE, height // 2 - GameConfig.CELL_SIZE,
                                24 * GameConfig.CELL_SIZE, 3 * GameConfig.CELL_SIZE, 10, 10)
        painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
        painter.setPen(QPen(QColor(255, 255, 255)))
        opacity = 0.7 + 0.3 * math.sin(self.game.screen_animation_frame * GameConfig.ANIMATION_SPEED)
        painter.setOpacity(opacity)
        painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height // 2, f"Очки: {self.game.state_manager.score}")
        painter.drawText(width // 2 - 10 * GameConfig.CELL_SIZE, height // 2 + GameConfig.CELL_SIZE,
                         "SPACE для рестарта | ESC для выхода")
        painter.setOpacity(1.0)

    def draw_pause_screen(self, painter, width, height):
        self.draw_background(painter, width, height)
        self.draw_map(painter, self.game.offset_x, self.game.offset_y)
        for ghost in self.game.ghosts:
            ghost.draw(painter, self.game.offset_x, self.game.offset_y)
        self.draw_pacman(painter, self.game.offset_x, self.game.offset_y, self.game.camera_scale)
        self.draw_hud(painter, width)
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, width, height)
        painter.setFont(QFont(GameConfig.FONT, int(GameConfig.CELL_SIZE * 2), QFont.Weight.Bold))
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(width // 2 - 6 * GameConfig.CELL_SIZE, height // 2, "ПАУЗА")
        painter.setFont(QFont(GameConfig.FONT, GameConfig.CELL_SIZE))
        painter.drawText(width // 2 - 8 * GameConfig.CELL_SIZE, height // 2 + 2 * GameConfig.CELL_SIZE,
                         "Нажми P для продолжения")
# === Основной класс игры ===

class PacmanGame(QWidget):
    """Основной класс игры Pac-Man."""
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("Pac-Man")
            self.state_manager = GameStateManager()
            self.renderer = Renderer(self)
            self.high_score_manager = HighScoreManager()
            self.pacman_x = 14
            self.pacman_y = 23
            self.pacman_direction = 'right'
            self.next_direction = 'right'
            self.pacman_animation_frame = 0
            self.screen_animation_frame = 0
            self.ghosts = [
                Ghost(13.5, 11, QColor(255, 0, 0), 'Blinky'),
                Ghost(14.5, 11, QColor(255, 184, 255), 'Pinky'),
                Ghost(13.5, 13, QColor(0, 255, 255), 'Inky')
            ]
            self.original_map = [row[:] for row in MAP_DATA]
            self.particles = []
            self.last_key = None
            self.last_key_time = 0
            self.sad_timer = 0
            self.camera_scale = 1.0
            self.last_frame_time = time.time()
            self.frame_count = 0
            self.current_fps = 60.0
            self.setup_ui()
            self.setup_timer()
            self.setup_sticky_cells()
            logging.info(f"Инициализация игры: Pac-Man на ({self.pacman_x}, {self.pacman_y}), призраков: {len(self.ghosts)}")
        except Exception as e:
            logging.error(f"Ошибка инициализации: {e}")
            sys.exit(1)

    def setup_ui(self):
        screen = QApplication.primaryScreen().geometry()
        scale_factor = min(screen.width() / (GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE),
                           screen.height() / (GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE))
        GameConfig.CELL_SIZE = int(GameConfig.CELL_SIZE * scale_factor)
        self.setFixedSize(screen.width(), screen.height())
        self.offset_x = (screen.width() - GameConfig.MAP_WIDTH * GameConfig.CELL_SIZE) // 2
        self.offset_y = (screen.height() - GameConfig.MAP_HEIGHT * GameConfig.CELL_SIZE) // 2
        self.showFullScreen()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.setInterval(1000 // GameConfig.FPS)
        self.timer.start()

    def setup_sticky_cells(self):
        available = [(x, y) for y in range(GameConfig.MAP_HEIGHT) for x in range(GameConfig.MAP_WIDTH)
                     if MAP_DATA[y][x] == 0]
        sticky_count = max(1, int(len(available) * 0.005))
        for x, y in random.sample(available, sticky_count):
            MAP_DATA[y][x] = 5
            logging.info(f"Липкая клетка добавлена на ({x}, {y})")

    def keyPressEvent(self, event):
        try:
            key = event.key()
            current_time = time.time()
            if self.state_manager.state == GameState.START:
                if key == Qt.Key.Key_Space:
                    self.state_manager.state = GameState.PLAYING
                elif key == Qt.Key.Key_Escape:
                    self.close()
            elif self.state_manager.state == GameState.PLAYING:
                if key in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down):
                    direction = {
                        Qt.Key.Key_Left: 'left',
                        Qt.Key.Key_Right: 'right',
                        Qt.Key.Key_Up: 'up',
                        Qt.Key.Key_Down: 'down'
                    }[key]
                    self.next_direction = direction
                    if (self.last_key == key and
                            current_time - self.last_key_time < 0.2 and
                            self.state_manager.dash_cooldown <= 0):
                        self.state_manager.dash_timer = 10
                        self.state_manager.dash_cooldown = GameConfig.DASH_COOLDOWN
                        logging.info("Рывок активирован")
                        dx, dy = DIRECTIONS[direction]
                        for _ in range(5):
                            self.particles.append(Particle(
                                self.pacman_x * GameConfig.CELL_SIZE,
                                self.pacman_y * GameConfig.CELL_SIZE,
                                -dx * random.uniform(1, 2),
                                -dy * random.uniform(1, 2),
                                GameConfig.PRIMARY_COLOR,
                                20
                            ))
                    self.last_key = key
                    self.last_key_time = current_time
                elif key == Qt.Key.Key_S and self.state_manager.shield_available and not self.state_manager.shield_active:
                    self.state_manager.shield_active = True
                    self.state_manager.shield_available = False
                    logging.info("Щит активирован")
                elif key == Qt.Key.Key_P:
                    self.state_manager.state = GameState.PAUSED
                elif key == Qt.Key.Key_Escape:
                    self.close()
            elif self.state_manager.state == GameState.PAUSED:
                if key == Qt.Key.Key_P:
                    self.state_manager.state = GameState.PLAYING
                elif key == Qt.Key.Key_Escape:
                    self.close()
            elif self.state_manager.state in (GameState.GAME_OVER, GameState.WIN):
                if key == Qt.Key.Key_Space:
                    self.reset_game()
                elif key == Qt.Key.Key_Escape:
                    self.close()
        except Exception as e:
            logging.error(f"Ошибка обработки нажатия клавиши: {e}")

    def can_move_to(self, x, y):
        try:
            grid_x, grid_y = int(round(x)), int(round(y))
            if not (0 <= grid_x < GameConfig.MAP_WIDTH and 0 <= grid_y < GameConfig.MAP_HEIGHT):
                return False
            return MAP_DATA[grid_y][grid_x] not in (1, 4) or self.state_manager.super_timer > 0
        except Exception as e:
            logging.error(f"Ошибка проверки движения: {e}")
            return False

    def move_pacman(self):
        try:
            speed_multiplier = 1 + 0.005 * (self.state_manager.pellets_eaten // 10)
            speed_multiplier = min(speed_multiplier, 1.2)
            current_speed = (
                GameConfig.PACMAN_SUPER_SPEED if self.state_manager.super_timer > 0 else
                GameConfig.PACMAN_DASH_SPEED if self.state_manager.dash_timer > 0 else
                GameConfig.PACMAN_BOOST_SPEED if self.state_manager.boost_timer > 0 else
                GameConfig.PACMAN_SPEED
            ) * speed_multiplier
            if self.state_manager.sticky_timer > 0:
                current_speed *= 0.5
            if (abs(self.pacman_x - round(self.pacman_x)) < current_speed * 2 and
                    abs(self.pacman_y - round(self.pacman_y)) < current_speed * 2):
                dx, dy = DIRECTIONS[self.next_direction]
                if self.can_move_to(self.pacman_x + dx * current_speed, self.pacman_y + dy * current_speed):
                    self.pacman_direction = self.next_direction
            dx, dy = DIRECTIONS[self.pacman_direction]
            new_x, new_y = self.pacman_x + dx * current_speed, self.pacman_y + dy * current_speed
            if self.can_move_to(new_x, new_y):
                self.pacman_x, self.pacman_y = new_x, new_y
                grid_x, grid_y = int(round(self.pacman_x)), int(round(self.pacman_y))
                if 0 <= grid_y < GameConfig.MAP_HEIGHT and 0 <= grid_x < GameConfig.MAP_WIDTH:
                    if MAP_DATA[grid_y][grid_x] == 2:
                        MAP_DATA[grid_y][grid_x] = 0
                        self.state_manager.score += 10
                        self.state_manager.pellets_eaten += 1
                        self.state_manager.boost_timer = GameConfig.BOOST_DURATION
                        logging.info(f"Съеден пеллет на ({grid_x}, {grid_y}), очки: {self.state_manager.score}")
                        if GameConfig.ENABLE_EFFECTS:
                            for _ in range(3):
                                angle = random.uniform(0, 2 * math.pi)
                                self.particles.append(Particle(
                                    self.pacman_x * GameConfig.CELL_SIZE,
                                    self.pacman_y * GameConfig.CELL_SIZE,
                                    math.cos(angle) * 2,
                                    math.sin(angle) * 2,
                                    GameConfig.PELLET_COLOR,
                                    15
                                ))
                    elif MAP_DATA[grid_y][grid_x] == 3:
                        MAP_DATA[grid_y][grid_x] = 0
                        self.state_manager.score += 50
                        self.state_manager.power_pellets_eaten += 1
                        self.state_manager.super_timer = GameConfig.SUPER_DURATION
                        for ghost in self.ghosts:
                            ghost.behavior = 'frightened'
                            ghost.frightened_timer = GameConfig.MODE_DURATIONS['frightened'] * GameConfig.FPS
                        logging.info(f"Съеден силовой пеллет на ({grid_x}, {grid_y}), суперрежим активирован")
                    elif MAP_DATA[grid_y][grid_x] == 5:
                        self.state_manager.sticky_timer = 3 * GameConfig.FPS
                        logging.info(f"Pac-Man на липкой клетке ({grid_x}, {grid_y})")
            if self.pacman_x < -0.5:
                self.pacman_x = GameConfig.MAP_WIDTH - 0.5
            elif self.pacman_x >= GameConfig.MAP_WIDTH + 0.5:
                self.pacman_x = -0.5
            teleport_positions = [(1, 15), (26, 15)]
            for tx, ty in teleport_positions:
                if abs(self.pacman_x - tx) < 0.5 and abs(self.pacman_y - ty) < 0.5:
                    other_tx, other_ty = teleport_positions[1 - teleport_positions.index((tx, ty))]
                    self.pacman_x, self.pacman_y = other_tx, other_ty
                    logging.info(f"Телепортация Pac-Man с ({tx}, {ty}) на ({other_tx}, {other_ty})")
                    break
            if self.state_manager.fruit_active:
                fruit_x, fruit_y = self.state_manager.fruit_x, self.state_manager.fruit_y
                if abs(self.pacman_x - fruit_x) < 0.5 and abs(self.pacman_y - fruit_y) < 0.5:
                    self.state_manager.fruit_active = False
                    self.state_manager.fruits_collected += 1
                    self.state_manager.score += GameConfig.FRUIT_SCORE
                    if self.state_manager.fruits_collected >= GameConfig.MAX_FRUITS_PER_LEVEL:
                        self.state_manager.score += GameConfig.SECRET_FRUIT_BONUS
                        logging.info("Секретный бонус за все фрукты!")
                    logging.info(f"Съеден фрукт на ({fruit_x}, {fruit_y}), очки: {self.state_manager.score}")
                    if GameConfig.ENABLE_EFFECTS:
                        for _ in range(5):
                            angle = random.uniform(0, 2 * math.pi)
                            self.particles.append(Particle(
                                self.pacman_x * GameConfig.CELL_SIZE,
                                self.pacman_y * GameConfig.CELL_SIZE,
                                math.cos(angle) * 3,
                                math.sin(angle) * 3,
                                GameConfig.FRUIT_COLOR,
                                20
                            ))
            logging.debug(f"Pac-Man: позиция ({self.pacman_x:.2f}, {self.pacman_y:.2f}), направление {self.pacman_direction}")
        except Exception as e:
            logging.error(f"Ошибка движения Pac-Man: {e}")

    def check_collisions(self):
        try:
            for ghost in self.ghosts:
                if (abs(self.pacman_x - ghost.x) < 0.5 and abs(self.pacman_y - ghost.y) < 0.5 and
                        not self.state_manager.shield_active):
                    if ghost.behavior == 'frightened':
                        self.state_manager.score += 200
                        ghost.x, ghost.y = ghost.home_x, ghost.home_y
                        ghost.behavior = 'chase'
                        ghost.path = []
                        logging.info(f"Съеден призрак {ghost.name}, очки: {self.state_manager.score}")
                        if GameConfig.ENABLE_EFFECTS:
                            for _ in range(10):
                                angle = random.uniform(0, 2 * math.pi)
                                self.particles.append(Particle(
                                    ghost.x * GameConfig.CELL_SIZE,
                                    ghost.y * GameConfig.CELL_SIZE,
                                    math.cos(angle) * 4,
                                    math.sin(angle) * 4,
                                    ghost.color,
                                    30
                                ))
                    else:
                        self.state_manager.lives -= 1
                        self.sad_timer = GameConfig.FPS
                        self.pacman_x, self.pacman_y = 14, 23
                        self.pacman_direction = 'right'
                        self.next_direction = 'right'
                        for ghost in self.ghosts:
                            ghost.x, ghost.y = ghost.home_x, ghost.home_y
                            ghost.behavior = 'chase'
                            ghost.path = []
                        logging.info(f"Столкновение с призраком {ghost.name}, жизни: {self.state_manager.lives}")
                        if self.state_manager.lives <= 0:
                            self.state_manager.state = GameState.GAME_OVER
                            self.high_score_manager.save_high_score(self.state_manager.score)
                            logging.info("Игра окончена")
                            return
        except Exception as e:
            logging.error(f"Ошибка проверки столкновений: {e}")

    def spawn_fruit(self):
        try:
            if (not self.state_manager.fruit_active and
                    self.state_manager.fruits_collected < GameConfig.MAX_FRUITS_PER_LEVEL and
                    random.random() < 1 / GameConfig.FRUIT_SPAWN_INTERVAL):
                available = [(x, y) for y in range(GameConfig.MAP_HEIGHT) for x in range(GameConfig.MAP_WIDTH)
                             if MAP_DATA[y][x] == 0]
                if available:
                    self.state_manager.fruit_x, self.state_manager.fruit_y = random.choice(available)
                    self.state_manager.fruit_active = True
                    logging.info(f"Фрукт появился на ({self.state_manager.fruit_x}, {self.state_manager.fruit_y})")
        except Exception as e:
            logging.error(f"Ошибка спавна фрукта: {e}")

    def reset_game(self):
        try:
            self.state_manager.reset()
            self.pacman_x, self.pacman_y = 14, 23
            self.pacman_direction = 'right'
            self.next_direction = 'right'
            for ghost in self.ghosts:
                ghost.x, ghost.y = ghost.home_x, ghost.home_y
                ghost.behavior = 'chase'
                ghost.path = []
            MAP_DATA[:] = [row[:] for row in self.original_map]
            self.particles = []
            self.sad_timer = 0
            self.setup_sticky_cells()
            logging.info("Игра сброшена")
        except Exception as e:
            logging.error(f"Ошибка сброса игры: {e}")

    def next_level(self):
        try:
            self.state_manager.level += 1
            self.state_manager.pellets_eaten = 0
            self.state_manager.fruits_collected = 0
            self.pacman_x, self.pacman_y = 14, 23
            self.pacman_direction = 'right'
            self.next_direction = 'right'
            for ghost in self.ghosts:
                ghost.x, ghost.y = ghost.home_x, ghost.home_y
                ghost.behavior = 'chase'
                ghost.path = []
            MAP_DATA[:] = [row[:] for row in self.original_map]
            self.state_manager.fruit_active = False
            self.particles = []
            self.state_manager.boost_timer = 0
            self.state_manager.dash_timer = 0
            self.state_manager.dash_cooldown = 0
            self.state_manager.super_timer = 0
            self.state_manager.shield_active = False
            self.state_manager.shield_available = True
            self.state_manager.sticky_timer = 0
            self.renderer.start_level_transition()
            self.setup_sticky_cells()
            logging.info(f"Переход на уровень {self.state_manager.level}")
        except Exception as e:
            logging.error(f"Ошибка перехода на следующий уровень: {e}")

    def game_loop(self):
        try:
            if self.state_manager.state == GameState.PLAYING:
                self.state_manager.switch_mode()
                self.move_pacman()
                blinky = next((g for g in self.ghosts if g.name == 'Blinky'), None)
                blinky_x, blinky_y = (blinky.x, blinky.y) if blinky else (0, 0)
                for ghost in self.ghosts:
                    ghost.update(
                        self.pacman_x, self.pacman_y, self.pacman_direction, self.next_direction,
                        blinky_x, blinky_y, self.state_manager.level, self.ghosts,
                        self.state_manager.dash_timer > 0
                    )
                self.check_collisions()
                self.spawn_fruit()
                self.pacman_animation_frame += 1
                self.particles = [p for p in self.particles if p.age < p.lifetime]
                for particle in self.particles:
                    particle.update()
                if self.state_manager.pellets_eaten >= GameConfig.TOTAL_PELLETS:
                    self.state_manager.state = GameState.WIN
                    self.high_score_manager.save_high_score(self.state_manager.score)
                    logging.info("Победа!")
                if self.state_manager.boost_timer > 0:
                    self.state_manager.boost_timer -= 1
                if self.state_manager.dash_timer > 0:
                    self.state_manager.dash_timer -= 1
                if self.state_manager.dash_cooldown > 0:
                    self.state_manager.dash_cooldown -= 1
                if self.state_manager.super_timer > 0:
                    self.state_manager.super_timer -= 1
                if self.state_manager.shield_active:
                    self.state_manager.shield_timer = self.state_manager.shield_timer - 1 if hasattr(self.state_manager, 'shield_timer') else GameConfig.SHIELD_DURATION
                    if self.state_manager.shield_timer <= 0:
                        self.state_manager.shield_active = False
                        self.state_manager.shield_timer = 0
                if self.state_manager.sticky_timer > 0:
                    self.state_manager.sticky_timer -= 1
                if self.sad_timer > 0:
                    self.sad_timer -= 1
            self.screen_animation_frame += 1
            current_time = time.time()
            self.frame_count += 1
            if current_time - self.last_frame_time >= 1:
                self.current_fps = self.frame_count / (current_time - self.last_frame_time)
                self.frame_count = 0
                self.last_frame_time = current_time
            self.renderer.transition_timer = max(0, self.renderer.transition_timer - 1)
            self.update()
        except Exception as e:
            logging.error(f"Ошибка игрового цикла: {e}")

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            width, height = self.width(), self.height()
            if self.state_manager.state == GameState.START:
                self.renderer.draw_start_screen(painter, width, height)
            elif self.state_manager.state == GameState.PLAYING:
                self.renderer.draw_background(painter, width, height)
                self.renderer.draw_map(painter, self.offset_x, self.offset_y)
                for ghost in self.ghosts:
                    ghost.draw(painter, self.offset_x, self.offset_y)
                self.renderer.draw_pacman(painter, self.offset_x, self.offset_y, self.camera_scale)
                for particle in self.renderer.transition_particles:
                    particle.update()
                    particle.draw(painter, self.offset_x, self.offset_y)
                self.renderer.transition_particles = [p for p in self.renderer.transition_particles if p.age < p.lifetime]
                self.renderer.draw_hud(painter, width)
            elif self.state_manager.state == GameState.PAUSED:
                self.renderer.draw_pause_screen(painter, width, height)
            elif self.state_manager.state in (GameState.GAME_OVER, GameState.WIN):
                self.renderer.draw_game_over_win(painter, width, height)
            painter.end()
        except Exception as e:
            logging.error(f"Ошибка отрисовки: {e}")

# === Запуск игры ===

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        game = PacmanGame()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Ошибка запуска приложения: {e}")
        sys.exit(1)