import pygame
from utils import (
    BG_COLOR, HEADER_COLOR, WHITE, BLACK, GRAY, DARK_GRAY,
    GREEN_FLASH, RED_FLASH, ANSWER_COLORS, ANSWER_HOVER_COLORS, ANSWER_ICONS,
    get_font, load_flag, draw_text_centered, draw_rounded_rect, timer_color,
)
from data import TIMER_SECONDS


W, H = 1024, 768


class Screen:
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, surface): pass
    def next_screen(self): return None


class MenuScreen(Screen):
    def __init__(self):
        self._name = ""
        self._cursor_visible = True
        self._cursor_timer = 0
        self._go = False
        self._font_big   = get_font(72, bold=True)
        self._font_med   = get_font(36, bold=True)
        self._font_small = get_font(28)
        self._font_input = get_font(32)
        self._error = ""

        box_w, box_h = 420, 54
        self._box = pygame.Rect((W - box_w) // 2, 400, box_w, box_h)
        btn_w, btn_h = 260, 60
        self._btn = pygame.Rect((W - btn_w) // 2, 490, btn_w, btn_h)
        self._btn_hover = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._name = self._name[:-1]
                self._error = ""
            elif event.key == pygame.K_RETURN:
                self._try_start()
            elif event.unicode and len(self._name) < 20:
                self._name += event.unicode
                self._error = ""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn.collidepoint(event.pos):
                self._try_start()

    def _try_start(self):
        if self._name.strip():
            self._go = True
        else:
            self._error = "Please enter your name!"

    def update(self, dt):
        self._cursor_timer += dt
        if self._cursor_timer >= 0.5:
            self._cursor_visible = not self._cursor_visible
            self._cursor_timer = 0
        mx, my = pygame.mouse.get_pos()
        self._btn_hover = self._btn.collidepoint(mx, my)

    def draw(self, surface):
        surface.fill(BG_COLOR)

        draw_text_centered(surface, "🌍  FLAG QUIZ", self._font_big, WHITE, W // 2, 130)
        draw_text_centered(surface, "How well do you know the world's flags?",
                           self._font_small, GRAY, W // 2, 210)

        pygame.draw.line(surface, (120, 60, 200), (W // 2 - 300, 250), (W // 2 + 300, 250), 2)

        draw_text_centered(surface, "Enter Your Name", self._font_med, WHITE, W // 2, 360)

        pygame.draw.rect(surface, WHITE, self._box, border_radius=10)
        pygame.draw.rect(surface, (200, 180, 255), self._box, 3, border_radius=10)
        name_surf = self._font_input.render(self._name + ("|" if self._cursor_visible else " "), True, BLACK)
        surface.blit(name_surf, (self._box.x + 12, self._box.y + 11))

        if self._error:
            draw_text_centered(surface, self._error, self._font_small, (255, 100, 100), W // 2, 462)

        col = (90, 200, 120) if self._btn_hover else (50, 170, 90)
        draw_rounded_rect(surface, col, self._btn, 14)
        draw_text_centered(surface, "START", self._font_med, WHITE, self._btn.centerx, self._btn.centery)

        draw_text_centered(surface, "7 Rounds  ·  3 Difficulty Levels  ·  30 World Flags",
                           get_font(20), (180, 150, 220), W // 2, H - 40)

    def next_screen(self):
        if self._go:
            return DifficultyScreen(self._name.strip())
        return None


class DifficultyScreen(Screen):
    DIFFICULTIES = [
        ("easy",       "EASY",       "Common world flags",      (43,  163, 90),  (35, 140, 75)),
        ("hard",       "HARD",       "Less obvious flags",      (25,  118, 210), (20, 100, 190)),
        ("impossible", "IMPOSSIBLE", "Obscure & tricky flags",  (226, 27,  60),  (200, 20, 50)),
    ]

    def __init__(self, player_name: str):
        self._player_name = player_name
        self._chosen = None
        self._font_big   = get_font(54, bold=True)
        self._font_med   = get_font(36, bold=True)
        self._font_small = get_font(24)
        self._font_sub   = get_font(22)
        self._hover = None

        btn_w, btn_h = 500, 90
        start_y = 260
        gap = 120
        self._buttons = []
        for i, (key, label, desc, col, hcol) in enumerate(self.DIFFICULTIES):
            rect = pygame.Rect((W - btn_w) // 2, start_y + i * gap, btn_w, btn_h)
            self._buttons.append((key, label, desc, col, hcol, rect))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, label, desc, col, hcol, rect in self._buttons:
                if rect.collidepoint(event.pos):
                    self._chosen = key

    def update(self, dt):
        mx, my = pygame.mouse.get_pos()
        self._hover = None
        for key, label, desc, col, hcol, rect in self._buttons:
            if rect.collidepoint(mx, my):
                self._hover = key

    def draw(self, surface):
        surface.fill(BG_COLOR)
        draw_text_centered(surface, f"Hey {self._player_name}!", self._font_big, WHITE, W // 2, 90)
        draw_text_centered(surface, "Choose your difficulty", self._font_med, GRAY, W // 2, 160)
        pygame.draw.line(surface, (120, 60, 200), (W // 2 - 300, 200), (W // 2 + 300, 200), 2)

        for key, label, desc, col, hcol, rect in self._buttons:
            c = hcol if self._hover == key else col
            draw_rounded_rect(surface, c, rect, 16)
            draw_text_centered(surface, label, self._font_med, WHITE, rect.centerx, rect.centery - 10)
            draw_text_centered(surface, desc, self._font_sub, (220, 220, 220), rect.centerx, rect.centery + 22)

        draw_text_centered(surface, "7 rounds per game", self._font_small, (180, 150, 220), W // 2, H - 40)

    def next_screen(self):
        if self._chosen:
            from game import Game
            g = Game()
            g.start(self._player_name, self._chosen)
            return QuizScreen(g)
        return None


class QuizScreen(Screen):
    _RESULT_PAUSE = 1.5

    def __init__(self, game):
        self._game = game
        self._font_big   = get_font(32, bold=True)
        self._font_med   = get_font(28, bold=True)
        self._font_small = get_font(22)
        self._font_score = get_font(24, bold=True)

        self._time_left = float(TIMER_SECONDS)
        self._answered = False
        self._chosen_idx = None
        self._result = None
        self._result_timer = 0.0
        self._flag_surf = None
        self._hover_idx = None

        self._btn_rects = []
        self._load_question()

    def _load_question(self):
        ok = self._game.next_question()
        if not ok:
            return
        q = self._game.current_question
        self._flag_surf = load_flag(q["flag"]["code"])
        self._time_left = float(TIMER_SECONDS)
        self._answered = False
        self._chosen_idx = None
        self._result = None
        self._result_timer = 0.0
        self._build_buttons(q["options"])

    def _build_buttons(self, options):
        cols = 2
        btn_w, btn_h = 460, 90
        gap_x, gap_y = 20, 16
        start_x = (W - (cols * btn_w + gap_x)) // 2
        start_y = 520
        self._btn_rects = []
        for i, opt in enumerate(options):
            col_idx = i % cols
            row_idx = i // cols
            x = start_x + col_idx * (btn_w + gap_x)
            y = start_y + row_idx * (btn_h + gap_y)
            self._btn_rects.append(pygame.Rect(x, y, btn_w, btn_h))

    def handle_event(self, event):
        if self._answered:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            q = self._game.current_question
            for i, rect in enumerate(self._btn_rects):
                if rect.collidepoint(event.pos):
                    self._answered = True
                    self._chosen_idx = i
                    self._result = self._game.answer(q["options"][i], self._time_left)
                    self._result_timer = 0.0

    def update(self, dt):
        if self._answered:
            self._result_timer += dt
            return
        self._time_left -= dt
        if self._time_left <= 0:
            self._time_left = 0
            self._answered = True
            self._result = self._game.timeout()
            self._result_timer = 0.0
        mx, my = pygame.mouse.get_pos()
        self._hover_idx = None
        for i, rect in enumerate(self._btn_rects):
            if rect.collidepoint(mx, my):
                self._hover_idx = i

    def draw(self, surface):
        surface.fill(BG_COLOR)
        q = self._game.current_question
        if q is None:
            return

        pygame.draw.rect(surface, HEADER_COLOR, (0, 0, W, 64))
        round_txt = f"Round {self._game.round_num} / {len(self._game.questions)}"
        draw_text_centered(surface, round_txt, self._font_small, GRAY, W // 2, 32)
        score_surf = self._font_score.render(f"Score: {self._game.score}", True, WHITE)
        surface.blit(score_surf, (W - score_surf.get_width() - 20, 20))

        bar_h = 12
        fraction = self._time_left / TIMER_SECONDS
        full_w = W - 40
        bar_w = int(full_w * fraction)
        pygame.draw.rect(surface, DARK_GRAY, (20, 68, full_w, bar_h), border_radius=6)
        if bar_w > 0:
            pygame.draw.rect(surface, timer_color(fraction), (20, 68, bar_w, bar_h), border_radius=6)
        secs = self._font_small.render(f"{int(self._time_left)}s", True, WHITE)
        surface.blit(secs, (W // 2 - secs.get_width() // 2, 85))

        flag_area_y = 110
        flag_area_h = 360
        if self._flag_surf:
            fw = self._flag_surf.get_width()
            fh = self._flag_surf.get_height()
            scale = min(400 / fw, flag_area_h / fh, 1.0)
            disp_w = int(fw * scale)
            disp_h = int(fh * scale)
            if scale != 1.0:
                flag = pygame.transform.smoothscale(self._flag_surf, (disp_w, disp_h))
            else:
                flag = self._flag_surf
            flag_x = (W - disp_w) // 2
            flag_y = flag_area_y + (flag_area_h - disp_h) // 2
            shadow = pygame.Surface((disp_w + 8, disp_h + 8), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 80))
            surface.blit(shadow, (flag_x - 4, flag_y + 4))
            surface.blit(flag, (flag_x, flag_y))
            pygame.draw.rect(surface, WHITE, (flag_x, flag_y, disp_w, disp_h), 3)
        else:
            draw_text_centered(surface, "[Flag not available]", self._font_small, GRAY,
                               W // 2, flag_area_y + flag_area_h // 2)

        draw_text_centered(surface, "Which country does this flag belong to?",
                           self._font_big, WHITE, W // 2, 490)

        for i, (rect, opt) in enumerate(zip(self._btn_rects, q["options"])):
            if self._answered:
                if opt == q["correct"]:
                    col = GREEN_FLASH
                elif i == self._chosen_idx:
                    col = RED_FLASH
                else:
                    col = DARK_GRAY
            else:
                col = ANSWER_HOVER_COLORS[i] if self._hover_idx == i else ANSWER_COLORS[i]

            draw_rounded_rect(surface, col, rect, 14)
            icon_surf = self._font_med.render(ANSWER_ICONS[i], True, WHITE)
            surface.blit(icon_surf, (rect.x + 16, rect.centery - icon_surf.get_height() // 2))
            draw_text_centered(surface, opt, self._font_med, WHITE, rect.centerx + 14, rect.centery)

        if self._answered and self._result:
            if self._result["correct"]:
                msg = f"+{self._result['points_earned']} pts!"
                col = GREEN_FLASH
            else:
                msg = f"Correct: {self._result['answer']}"
                col = RED_FLASH
            draw_text_centered(surface, msg, get_font(30, bold=True), col, W // 2, 475)

    def next_screen(self):
        if self._answered and self._result_timer >= self._RESULT_PAUSE:
            if self._game.is_done:
                self._game.save_score()
                return LeaderboardScreen(self._game)
            else:
                return QuizScreen(self._game)
        return None


class LeaderboardScreen(Screen):
    def __init__(self, game):
        self._game = game
        self._font_big   = get_font(54, bold=True)
        self._font_med   = get_font(32, bold=True)
        self._font_row   = get_font(26)
        self._font_small = get_font(22)
        self._hover_play = False
        self._play_again = False
        self._quit = False

        btn_w, btn_h = 260, 60
        self._btn_play = pygame.Rect((W // 2) - btn_w - 20, H - 110, btn_w, btn_h)
        self._btn_quit = pygame.Rect((W // 2) + 20, H - 110, btn_w, btn_h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_play.collidepoint(event.pos):
                self._play_again = True
            if self._btn_quit.collidepoint(event.pos):
                self._quit = True

    def update(self, dt):
        mx, my = pygame.mouse.get_pos()
        self._hover_play = self._btn_play.collidepoint(mx, my)

    def draw(self, surface):
        surface.fill(BG_COLOR)
        draw_text_centered(surface, "GAME OVER!", self._font_big, WHITE, W // 2, 60)

        g = self._game
        diff_label = g.difficulty.upper()
        draw_text_centered(
            surface,
            f"{g.player_name}  —  {g.score} pts  ({diff_label})",
            self._font_med, (255, 215, 0), W // 2, 130,
        )
        pygame.draw.line(surface, (120, 60, 200), (W // 2 - 380, 165), (W // 2 + 380, 165), 2)

        board = g.leaderboard
        draw_text_centered(surface, "LEADERBOARD", self._font_med, GRAY, W // 2, 195)

        row_h = 44
        for idx, entry in enumerate(board[:8]):
            y = 235 + idx * row_h
            bg_col = (80, 30, 150) if entry["name"] == g.player_name and entry["score"] == g.score else (55, 20, 110)
            row_rect = pygame.Rect(W // 2 - 380, y, 760, row_h - 4)
            draw_rounded_rect(surface, bg_col, row_rect, 8)

            medal = ["🥇", "🥈", "🥉"][idx] if idx < 3 else f"#{idx+1}"
            rank_surf = self._font_row.render(str(medal), True, WHITE)
            surface.blit(rank_surf, (row_rect.x + 12, y + 8))

            name_surf = self._font_row.render(entry["name"], True, WHITE)
            surface.blit(name_surf, (row_rect.x + 80, y + 8))

            score_surf = self._font_row.render(f"{entry['score']} pts", True, (255, 215, 0))
            surface.blit(score_surf, (row_rect.right - score_surf.get_width() - 16, y + 8))

        play_col = (35, 140, 75) if self._hover_play else (43, 163, 90)
        draw_rounded_rect(surface, play_col, self._btn_play, 14)
        draw_text_centered(surface, "PLAY AGAIN", self._font_med, WHITE,
                           self._btn_play.centerx, self._btn_play.centery)

        draw_rounded_rect(surface, (100, 30, 60), self._btn_quit, 14)
        draw_text_centered(surface, "QUIT", self._font_med, WHITE,
                           self._btn_quit.centerx, self._btn_quit.centery)

    def next_screen(self):
        if self._quit:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return None
        if self._play_again:
            return MenuScreen()
        return None
