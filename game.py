import random
import sys
from collections import deque

import pygame

# Configuration Constants
BOARD_COLS = 40
BOARD_ROWS = 25
CELL_SIZE = 20
GRID_WIDTH = BOARD_COLS * CELL_SIZE
GRID_HEIGHT = BOARD_ROWS * CELL_SIZE
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT
FPS = 10

# Colors
COLOR_BG = (30, 30, 30)
COLOR_GRID = (40, 40, 40)
COLOR_BORDER = (60, 60, 60)
COLOR_SIDEBAR = (20, 20, 20)
COLOR_TEXT = (220, 220, 220)
COLOR_TEXT_DIM = (140, 140, 140)
COLOR_FOOD = (255, 80, 80)
COLOR_FOOD_GLOW = (255, 120, 120)
PLAYER_COLORS = [
    {"head": (80, 200, 120), "body": (50, 150, 90)},
    {"head": (80, 140, 255), "body": (50, 100, 200)},
    {"head": (255, 180, 60), "body": (200, 140, 40)},
]


def _glyph(*rows):
    return rows


BITMAP_FONT = {
    " ": _glyph(
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ),
    "?": _glyph(
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "00000",
        "00100",
    ),
    ":": _glyph(
        "00000",
        "00100",
        "00100",
        "00000",
        "00100",
        "00100",
        "00000",
    ),
    "/": _glyph(
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "00000",
        "00000",
    ),
    "-": _glyph(
        "00000",
        "00000",
        "00000",
        "11111",
        "00000",
        "00000",
        "00000",
    ),
    "0": _glyph(
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110",
    ),
    "1": _glyph(
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ),
    "2": _glyph(
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ),
    "3": _glyph(
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110",
    ),
    "4": _glyph(
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ),
    "5": _glyph(
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110",
    ),
    "6": _glyph(
        "01110",
        "10000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ),
    "7": _glyph(
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ),
    "8": _glyph(
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ),
    "9": _glyph(
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00001",
        "01110",
    ),
    "A": _glyph(
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ),
    "B": _glyph(
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ),
    "C": _glyph(
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110",
    ),
    "D": _glyph(
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ),
    "E": _glyph(
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ),
    "F": _glyph(
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ),
    "G": _glyph(
        "01110",
        "10001",
        "10000",
        "10000",
        "10011",
        "10001",
        "01110",
    ),
    "H": _glyph(
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ),
    "I": _glyph(
        "01110",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ),
    "J": _glyph(
        "00111",
        "00010",
        "00010",
        "00010",
        "10010",
        "10010",
        "01100",
    ),
    "K": _glyph(
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ),
    "L": _glyph(
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ),
    "M": _glyph(
        "10001",
        "11011",
        "10101",
        "10001",
        "10001",
        "10001",
        "10001",
    ),
    "N": _glyph(
        "10001",
        "11001",
        "10101",
        "10011",
        "10001",
        "10001",
        "10001",
    ),
    "O": _glyph(
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ),
    "P": _glyph(
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ),
    "Q": _glyph(
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101",
    ),
    "R": _glyph(
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ),
    "S": _glyph(
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ),
    "T": _glyph(
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ),
    "U": _glyph(
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ),
    "V": _glyph(
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100",
    ),
    "W": _glyph(
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "11011",
        "10001",
    ),
    "X": _glyph(
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001",
    ),
    "Y": _glyph(
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
    ),
    "Z": _glyph(
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111",
    ),
}


def render_bitmap_text(text, color, scale):
    lines = text.upper().split("\n")
    char_width = 5 * scale
    char_height = 7 * scale
    line_spacing = scale * 2
    char_spacing = scale

    widths = []
    for line in lines:
        if not line:
            widths.append(0)
        else:
            widths.append(len(line) * (char_width + char_spacing) - char_spacing)

    surface = pygame.Surface(
        (
            max(1, max(widths, default=0)),
            max(1, len(lines) * char_height + max(0, len(lines) - 1) * line_spacing),
        ),
        pygame.SRCALPHA,
    )

    y = 0
    for line in lines:
        x = 0
        for ch in line:
            glyph = BITMAP_FONT.get(ch, BITMAP_FONT["?"])
            for row_idx, row in enumerate(glyph):
                for col_idx, pixel in enumerate(row):
                    if pixel == "1":
                        pygame.draw.rect(
                            surface,
                            color,
                            (
                                x + col_idx * scale,
                                y + row_idx * scale,
                                scale,
                                scale,
                            ),
                        )
            x += char_width + char_spacing
        y += char_height + line_spacing

    return surface


class BitmapFont:
    def __init__(self, scale):
        self.scale = max(1, scale)

    def render(self, text, antialias, color):
        return render_bitmap_text(text, color, self.scale)


def create_font(size, bold=False):
    scale = 2 if size >= 24 else 1
    return BitmapFont(scale)


def get_all_controllers():
    """Initialize and return all connected joysticks."""
    controllers = []
    try:
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            controllers.append(joy)
    except Exception:
        pass
    return controllers


class Player:
    def __init__(self, player_id, start_x, start_y, is_ai=True, has_controller=False, controller_idx=-1):
        self.player_id = player_id
        self.body = deque([(start_x, start_y)])
        self.direction = (1, 0)
        self.score = 0
        self.is_alive = True
        self.is_ai = is_ai
        self.has_controller = has_controller
        self.controller_idx = controller_idx
        self._ai_direction_timer = 0
        self.position = (start_x, start_y)
        self.waiting_to_rejoin = False

    def set_direction(self, new_dir):
        current = self.direction
        if (new_dir[0] * -1, new_dir[1] * -1) != current:
            self.direction = new_dir

    def update_ai_direction(self, all_players, food_positions):
        if not self.is_ai or not self.is_alive:
            return

        self._ai_direction_timer += 1
        if self._ai_direction_timer < 3:
            return
        self._ai_direction_timer = 0

        head_x, head_y = self.get_head()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        safe_dirs = []
        for dx, dy in directions:
            if (dx * -1, dy * -1) == self.direction:
                continue
            nx = (head_x + dx) % BOARD_COLS
            ny = (head_y + dy) % BOARD_ROWS

            hit = False
            for p in all_players:
                if not p.is_alive:
                    continue
                for bx, by in p.body:
                    if (nx, ny) == (bx, by):
                        hit = True
                        break
                if hit:
                    break
            if not hit:
                safe_dirs.append((dx, dy))

        if not safe_dirs:
            return

        if food_positions:
            best_dir = None
            best_dist = float("inf")
            nearest_food = min(
                food_positions, key=lambda f: abs(f[0] - head_x) + abs(f[1] - head_y)
            )
            for dx, dy in safe_dirs:
                nx = (head_x + dx) % BOARD_COLS
                ny = (head_y + dy) % BOARD_ROWS
                dist = abs(nx - nearest_food[0]) + abs(ny - nearest_food[1])
                if dist < best_dist:
                    best_dist = dist
                    best_dir = (dx, dy)
            if best_dir:
                self.direction = best_dir
        else:
            self.direction = random.choice(safe_dirs)

    def move(self, eat_food=False):
        if not self.is_alive:
            return None

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % BOARD_COLS, (head_y + dy) % BOARD_ROWS)

        self.body.appendleft(new_head)

        if not eat_food and len(self.body) > 1:
            self.body.pop()

        return new_head

    def get_next_head(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        return ((head_x + dx) % BOARD_COLS, (head_y + dy) % BOARD_ROWS)

    def check_collision(self, all_players):
        if not self.is_alive:
            return True

        head_x, head_y = self.get_head()

        for p in all_players:
            if not p.is_alive:
                continue
            check_body = list(p.body)
            if p.player_id == self.player_id:
                check_body = check_body[1:]
            if (head_x, head_y) in check_body:
                self.is_alive = False
                if not self.is_ai:
                    self.waiting_to_rejoin = True
                return True

        return False

    def get_head(self):
        return self.body[0]


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, GRID_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font_large = create_font(24, bold=True)
        self.font_medium = create_font(18)
        self.font_small = create_font(14)
        self.players = []
        self.food = deque()
        self.game_over = False
        self.paused = True  # Start paused until ready
        self.high_score = 0
        self._initialize_players()
        self._place_food()

    def _initialize_players(self):
        controllers = get_all_controllers()
        # Keep joystick objects alive; keyed by controller_idx (device index)
        self._joysticks = {i: joy for i, joy in enumerate(controllers)}

        # Human player on keyboard
        self.players = [
            Player(1, BOARD_COLS // 4, BOARD_ROWS // 2, is_ai=False),
        ]

        # One human player per connected controller (up to 2 extra)
        for idx, _ in enumerate(controllers[:2]):
            pid = len(self.players) + 1
            x = BOARD_COLS * (idx + 2) // 3
            y = BOARD_ROWS // 4
            self.players.append(
                Player(pid, x, y, is_ai=False, has_controller=True, controller_idx=idx)
            )

        # Fill remaining slots with AI
        while len(self.players) < 3:
            pid = len(self.players) + 1
            x = BOARD_COLS * (len(self.players)) // 3
            y = BOARD_ROWS // 4
            self.players.append(Player(pid, x, y, is_ai=True))

    def _place_food(self, positions=None):
        if positions is None:
            candidates = []
            for x in range(BOARD_COLS):
                for y in range(BOARD_ROWS):
                    if (x, y) not in self.food:
                        is_safe = True
                        for player in self.players:
                            if (x, y) in player.body:
                                is_safe = False
                                break
                        if is_safe:
                            candidates.append((x, y))

        while len(self.food) < 3:
            if not positions:
                if not candidates:
                    return
                positions = candidates.copy()
                random.shuffle(positions)
            elif not positions:
                return

            if not positions:
                break

            x, y = positions.pop()
            self.food.append((x, y))

    def _get_food_positions(self):
        return list(self.food)

    def reset(self):
        # Reset all existing players
        for player in self.players:
            player.body.clear()
            player.score = 0
            player.is_alive = True
            player.direction = (1, 0)
            player._ai_direction_timer = 0
            player.waiting_to_rejoin = False

        # Reset new players based on their positions
        self.players[0].body = deque([(BOARD_COLS // 4, BOARD_ROWS // 2)])
        for i in range(1, len(self.players)):
            x, y = self.players[i].position
            self.players[i].body = deque([(x, y)])

        self.food.clear()
        self._place_food()
        self.game_over = False
        self.high_score = max(self.high_score, self.players[0].score)

    def _find_safe_spawn(self, preferred_pos):
        occupied = set()
        for p in self.players:
            if p.is_alive:
                occupied.update(p.body)
        occupied.update(self.food)
        if preferred_pos not in occupied:
            return preferred_pos
        candidates = [
            (x, y)
            for x in range(BOARD_COLS)
            for y in range(BOARD_ROWS)
            if (x, y) not in occupied
        ]
        return random.choice(candidates) if candidates else preferred_pos

    def _rejoin_player(self, player):
        if not any(p.is_alive for p in self.players):
            return
        spawn = self._find_safe_spawn(player.position)
        player.body = deque([spawn])
        player.is_alive = True
        player.waiting_to_rejoin = False
        player.score = 0
        player.direction = (1, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_p:
                    self.paused = not self.paused

                if self.game_over:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.reset()
                    continue

                player = self.players[0]
                if player.waiting_to_rejoin:
                    rejoin_keys = {
                        pygame.K_SPACE, pygame.K_RETURN,
                        pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                        pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                    }
                    if event.key in rejoin_keys:
                        self._rejoin_player(player)
                    continue

                if not player.is_alive:
                    continue

                dir_map = {
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_w: (0, -1),
                    pygame.K_s: (0, 1),
                    pygame.K_a: (-1, 0),
                    pygame.K_d: (1, 0),
                }

                if event.key in dir_map:
                    player.set_direction(dir_map[event.key])

            if event.type == pygame.JOYBUTTONDOWN:
                # Any button: restart, unpause, or rejoin
                if self.game_over:
                    self.reset()
                    continue
                if self.paused:
                    self.paused = False
                    continue
                for p in self.players:
                    if p.controller_idx == event.joy and p.waiting_to_rejoin:
                        self._rejoin_player(p)
                        break

        # Poll controller axes and D-pad each frame for direction
        if not self.game_over and not self.paused:
            for p in self.players:
                if not p.has_controller or not p.is_alive:
                    continue
                joy = self._joysticks.get(p.controller_idx)
                if joy is None:
                    continue
                try:
                    # D-pad has priority over stick
                    hx, hy = joy.get_hat(0) if joy.get_numhats() > 0 else (0, 0)
                    if hx != 0:
                        p.set_direction((hx, 0))
                    elif hy != 0:
                        p.set_direction((0, -hy))  # hat y is inverted vs screen
                    else:
                        ax = joy.get_axis(0)
                        ay = joy.get_axis(1)
                        if abs(ax) > 0.5 and abs(ax) >= abs(ay):
                            p.set_direction((1, 0) if ax > 0 else (-1, 0))
                        elif abs(ay) > 0.5:
                            p.set_direction((0, 1) if ay > 0 else (0, -1))
                except Exception:
                    pass

        # Poll buttons for restart / unpause / rejoin
        for p in self.players:
            if not p.has_controller:
                continue
            joy = self._joysticks.get(p.controller_idx)
            if joy is None:
                continue
            try:
                any_pressed = any(joy.get_button(b) for b in range(joy.get_numbuttons()))
                if any_pressed:
                    if not hasattr(p, '_btn_was_pressed') or not p._btn_was_pressed:
                        p._btn_was_pressed = True
                        if self.game_over:
                            self.reset()
                            break
                        if self.paused:
                            self.paused = False
                        elif p.waiting_to_rejoin:
                            self._rejoin_player(p)
                else:
                    p._btn_was_pressed = False
            except Exception:
                pass

        return True

    def process_game_tick(self):
        if self.game_over or self.paused:
            return

        food_positions = self._get_food_positions()
        for player in self.players:
            if player.is_ai:
                player.update_ai_direction(self.players, food_positions)

        food_eaten = set()

        for player in self.players:
            if not player.is_alive:
                continue

            next_head = player.get_next_head()
            ate_food = next_head in self.food
            if ate_food:
                food_eaten.add(next_head)

            player.move(eat_food=ate_food)

            if player.check_collision(self.players):
                continue

            if ate_food and player.is_alive:
                player.score += 10
                if next_head in self.food:
                    self.food.remove(next_head)

        if food_eaten:
            self._place_food()

        alive_players = [p for p in self.players if p.is_alive]
        if not alive_players:
            self.game_over = True
            for p in self.players:
                if not p.is_ai:
                    self.high_score = max(self.high_score, p.score)

    def draw_grid(self):
        for x in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (GRID_WIDTH, y))

        pygame.draw.rect(
            self.screen,
            COLOR_BORDER,
            (0, 0, GRID_WIDTH, GRID_HEIGHT),
            2,
        )

    def draw_snake(self, player):
        colors = PLAYER_COLORS[player.player_id - 1]
        # Highlight human player's snake in green border
        highlight_color = (0, 255, 0) if not player.is_ai else (50, 50, 50)

        for i, (x, y) in enumerate(player.body):
            rect = pygame.Rect(
                x * CELL_SIZE + 1,
                y * CELL_SIZE + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2,
            )
            color = colors["head"] if i == 0 else colors["body"]
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

            # Add highlight border for human player
            if i == 0 and not player.is_alive:
                continue

            if not player.is_ai and i == 0:
                pygame.draw.rect(self.screen, highlight_color, rect, 2, border_radius=4)

            if i == 0 and player.is_alive:
                eye_size = 3
                dx, dy = player.direction
                cx = x * CELL_SIZE + CELL_SIZE // 2
                cy = y * CELL_SIZE + CELL_SIZE // 2

                if dx == 1:
                    offsets = [(4, -4), (4, 4)]
                elif dx == -1:
                    offsets = [(-4, -4), (-4, 4)]
                elif dy == -1:
                    offsets = [(-4, -4), (4, -4)]
                else:
                    offsets = [(-4, 4), (4, 4)]

                for ox, oy in offsets:
                    eye_rect = pygame.Rect(
                        cx + ox - eye_size // 2,
                        cy + oy - eye_size // 2,
                        eye_size,
                        eye_size,
                    )
                    pygame.draw.rect(self.screen, (255, 255, 255), eye_rect)

    def draw_food(self):
        pulse = int(pygame.time.get_ticks() / 200) % 2
        color = COLOR_FOOD_GLOW if pulse else COLOR_FOOD

        for x, y in self.food:
            rect = pygame.Rect(
                x * CELL_SIZE + 2,
                y * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            )
            pygame.draw.rect(self.screen, color, rect, border_radius=CELL_SIZE // 2)

    def _draw_icon(self, x, y, icon_name, size=12):
        icon = self.font_small.render(icon_name, True, COLOR_TEXT)
        icon_x = x - icon.get_width() // 2
        icon_y = y - size // 2
        self.screen.blit(icon, (icon_x, icon_y))

    def draw_sidebar(self):
        sidebar_x = GRID_WIDTH
        pygame.draw.rect(
            self.screen, COLOR_SIDEBAR, (sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        )
        pygame.draw.line(
            self.screen,
            COLOR_BORDER,
            (GRID_WIDTH, 0),
            (GRID_WIDTH, WINDOW_HEIGHT),
            2,
        )

        y = 20
        title = self.font_large.render("SNAKE", True, COLOR_TEXT)
        self.screen.blit(title, (sidebar_x + 50, y))
        y += 35

        # High score display at top
        high_score_text = self.font_medium.render(
            f"HIGH: {self.high_score}", True, (200, 200, 100)
        )
        self.screen.blit(high_score_text, (sidebar_x + 15, y))
        y += 20

        pygame.draw.line(
            self.screen,
            COLOR_BORDER,
            (sidebar_x + 10, y),
            (sidebar_x + SIDEBAR_WIDTH - 10, y),
        )
        y += 15

        # Food counter and combo display
        food_count = len(self.food)
        food_text = self.font_medium.render(f"Food: {food_count}", True, COLOR_TEXT_DIM)
        self.screen.blit(food_text, (sidebar_x + 15, y))
        y += 20

        for player in self.players:
            label = "YOU" if not player.is_ai else f"P{player.player_id}"
            player_icon = "🤖" if player.is_ai else "👤"

            full_label = f"{player_icon} {label}" if player.is_ai else label
            if player.waiting_to_rejoin:
                status = "REJOIN?"
            else:
                status = "ALIVE" if player.is_alive else "DEAD"
            color = PLAYER_COLORS[player.player_id - 1]["head"]

            name_surf = self.font_medium.render(full_label, True, color)
            self.screen.blit(name_surf, (sidebar_x + 15, y))
            y += 18

            # Add progress bar for snake length
            max_length = 40
            progress = min(100, player.score // (max_length - 1))
            pygame.draw.rect(
                self.screen,
                COLOR_SIDEBAR,
                (sidebar_x + 15, y - 8, SIDEBAR_WIDTH - 30, 6),
            )
            pygame.draw.rect(
                self.screen,
                color if player.is_alive else (150, 50, 50),
                (sidebar_x + 17, y - 6, max(1, progress), 4),
            )
            y += 16

            score_surf = self.font_small.render(
                f"Score: {player.score}", True, COLOR_TEXT_DIM
            )
            self.screen.blit(score_surf, (sidebar_x + 25, y))
            y += 16

            status_color = color if player.is_alive else (150, 50, 50)
            if player.waiting_to_rejoin:
                status_color = (255, 220, 80)
            status_surf = self.font_small.render(status, True, status_color)
            self.screen.blit(status_surf, (sidebar_x + 25, y))
            y += 18

        y += 8
        pygame.draw.line(
            self.screen,
            COLOR_BORDER,
            (sidebar_x + 10, y),
            (sidebar_x + SIDEBAR_WIDTH - 10, y),
        )
        y += 15

        controls = [
            "CONTROLS",
            "ARROWS / WASD",
            "P - PAUSE",
            "ESC - QUIT",
        ]
        for line in controls:
            surf = self.font_small.render(line, True, COLOR_TEXT_DIM)
            self.screen.blit(surf, (sidebar_x + 15, y))
            y += 18

        y += 5
        control_text = self.font_small.render("YOU: GREEN BORDER", True, (0, 255, 0))
        control_text.set_alpha(180)
        self.screen.blit(control_text, (sidebar_x + 15, y))

    def draw_game_over(self):
        overlay = pygame.Surface((GRID_WIDTH, GRID_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("GAME OVER", True, (255, 80, 80))
        rect = text.get_rect(center=(GRID_WIDTH // 2, GRID_HEIGHT // 2 - 30))
        self.screen.blit(text, rect)

        score = self.players[0].score
        score_text = self.font_medium.render(f"Score: {score}", True, COLOR_TEXT)
        score_rect = score_text.get_rect(
            center=(GRID_WIDTH // 2, GRID_HEIGHT // 2 + 10)
        )
        self.screen.blit(score_text, score_rect)

        prompt = self.font_small.render(
            "Press SPACE or ENTER to restart", True, COLOR_TEXT_DIM
        )
        prompt_rect = prompt.get_rect(center=(GRID_WIDTH // 2, GRID_HEIGHT // 2 + 50))
        self.screen.blit(prompt, prompt_rect)

    def draw_paused(self):
        overlay = pygame.Surface((GRID_WIDTH, GRID_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("PAUSED", True, COLOR_TEXT)
        rect = text.get_rect(center=(GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.screen.blit(text, rect)

    def draw_rejoin_prompt(self):
        if not any(p.waiting_to_rejoin for p in self.players):
            return
        msg = "PRESS SPACE / BTN TO REJOIN"
        surf = self.font_small.render(msg, True, (255, 220, 80))
        rect = surf.get_rect(center=(GRID_WIDTH // 2, GRID_HEIGHT - 20))
        bg = pygame.Rect(rect.x - 6, rect.y - 4, rect.width + 12, rect.height + 8)
        pygame.draw.rect(self.screen, (20, 20, 20), bg, border_radius=4)
        self.screen.blit(surf, rect)

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_grid()
        self.draw_food()

        for player in self.players:
            if player.is_alive:
                self.draw_snake(player)

        self.draw_sidebar()

        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_paused()
        else:
            self.draw_rejoin_prompt()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.process_game_tick()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
