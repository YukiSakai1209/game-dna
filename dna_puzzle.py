import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "DNA Puzzle! 男の子？女の子？"

# Colors
BACKGROUND_COLOR = (200, 200, 200)  # Light gray
PLACEHOLDER_COLOR_1 = (150, 150, 250)  # Light blue (Chromosome List)
PLACEHOLDER_COLOR_2 = (250, 150, 150)  # Light red (Karyotype Area)
TEXT_COLOR = (0, 0, 0)  # Black
BUTTON_COLOR = (100, 200, 100) # Greenish
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_HOVER_COLOR = (150, 250, 150)

# Create the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Initialize Pygame Mixer
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Warning: Could not initialize sound mixer. Sound will be disabled. Error: {e}")

# Font for labels
font = pygame.font.Font(None, 36) 
small_font = pygame.font.Font(None, 24)
placeholder_font = pygame.font.Font(None, 18)
mistake_font = pygame.font.Font(None, 30)
trivia_font_title = pygame.font.Font(None, 28)
trivia_font_text = pygame.font.Font(None, 22)
button_font = pygame.font.Font(None, 32)
results_font = pygame.font.Font(None, 48)
message_font = pygame.font.Font(None, 30)


# Chromosome dimensions
CHROMOSOME_WIDTH = 30
CHROMOSOME_HEIGHT = 50
CHROMOSOME_BORDER_COLOR = (50, 50, 50)
CHROMOSOME_PLACEHOLDER_BG = (100, 100, 120)

# --- Game Setup ---
current_gender = random.choice(['male', 'female'])
TRIVIA_DISPLAY_DURATION = 7000  # milliseconds

# --- Game State Variables ---
game_state = 'INITIALIZING' # INITIALIZING, PUZZLE, GUESSING, RESULTS
game_start_time = 0
puzzle_completion_time = 0
gender_guess_correct = None
final_score = 0
result_message = ""
score_message = ""

# --- Guessing UI ---
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 60
BUTTON_PADDING = 20
male_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH - BUTTON_PADDING // 2,
    SCREEN_HEIGHT // 2,
    BUTTON_WIDTH, BUTTON_HEIGHT
)
female_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 + BUTTON_PADDING // 2,
    SCREEN_HEIGHT // 2,
    BUTTON_WIDTH, BUTTON_HEIGHT
)

# --- Gene Loci Trivia Data (Kid-friendly) ---
GENE_LOCI_TRIVIA = [
    {"gene_name": "きみの けつえきがた", "chromosome_type": "9", "explanation": "きみの けつえきがたを きめている いでんしだよ。", "trait": "とくちょう: A, B, O, ABがたの けつえきがたが あるね。"},
    {"gene_name": "いろの みえかた", "chromosome_type": "X", "explanation": "あかや みどりの いろの みえかたに かんけいするよ。", "trait": "とくちょう: ひとによって、すこしだけ いろの みえかたが ちがうことが あるんだ。"},
    {"gene_name": "ぎゅうにゅうを のむちから", "chromosome_type": "2", "explanation": "ぎゅうにゅうを のんだあと、おなかが ゴロゴロしちゃうか きめる いでんし。", "trait": "とくちょう: おとなに なっても ぎゅうにゅうを ごくごく のめるかな？"},
    {"gene_name": "おさけの つよさ", "chromosome_type": "12", "explanation": "おとなに なったとき、おさけに よいやすいか どうかに かんけいするよ。", "trait": "とくちょう: これは まだ さきの はなしだけどね！"},
    {"gene_name": "おとこのこに なるスイッチ", "chromosome_type": "Y", "explanation": "この いでんしが あると、おとこのこに なるんだ。とても だいじな スイッチだね。", "trait": "とくちょう: Yせんしょくたい だけが もっているんだ。"},
    {"gene_name": "みみあかの タイプ", "chromosome_type": "16", "explanation": "みみあかが カサカサか、ベトベトか に かんけいする いでんし。", "trait": "とくちょう: びっくりするけど、これも いでんで きまるんだよ！"},
    {"gene_name": "かみのけの しつ", "chromosome_type": "1", "explanation": "かみのけが まっすぐか、くるくるか に かんけいするよ。", "trait": "とくちょう: ストレートヘアも、てんねんパーマも、いでんしが きめているんだ。"},
    {"gene_name": "ひかりで くしゃみ", "chromosome_type": "2", "explanation": "つよい ひかりを みると、くしゃみが でるか どうかに かんけいするよ。", "trait": "とくちょう: たいようを みあげて「ハックション！」となるのは、いでんしかも？"},
    {"gene_name": "そばかす", "chromosome_type": "16", "explanation": "ひに あたると、かおや うでに できる ちいさな てんてん。", "trait": "とくちょう: この いでんしを もっていると、そばかすが できやすいんだ。"},
    {"gene_name": "ふしぎな におい", "chromosome_type": "1", "explanation": "アスパラガスを たべたあと、おしっこの においが わかるかな？", "trait": "とくちょう: においを かんじる人と かんじない人が いる、ふしぎな いでんしだよ。"}
]

# --- Chromosome Data ---
MALE_CHROMOSOME_FILENAMES = [(f"male_chr{i:02d}_a.png", f"{i}a") for i in range(1,23)] + [(f"male_chr{i:02d}_b.png", f"{i}b") for i in range(1,23)] + [("male_X.png", "X"), ("male_Y.png", "Y")]
FEMALE_CHROMOSOME_FILENAMES = [(f"female_chr{i:02d}_a.png", f"{i}a") for i in range(1,23)] + [(f"female_chr{i:02d}_b.png", f"{i}b") for i in range(1,23)] + [("female_X_a.png", "Xa"), ("female_X_b.png", "Xb")]

def get_chromosome_type_from_id(id_name):
    if id_name.startswith("X") and len(id_name) > 1: return "X"
    if id_name[-1].isalpha() and id_name[:-1].isdigit(): return id_name[:-1]
    return id_name 

class Chromosome:
    def __init__(self, image, full_id_name, initial_pos_rect):
        self.image = image
        self.id_name = full_id_name 
        id_suffix = full_id_name.split('_')[-1] 
        self.correct_slot_type = get_chromosome_type_from_id(id_suffix)
        self.display_id = id_suffix 
        self.original_rect = initial_pos_rect.copy()
        self.current_rect = initial_pos_rect.copy()
        self.is_dragging = False
        self.is_placed = False
        self.slot_id = None 

draggable_chromosomes = [] 
karyotype_slots = [] 
placed_chromosomes_map = {} 

try:
    correct_sound = pygame.mixer.Sound("correct.wav")
    incorrect_sound = pygame.mixer.Sound("incorrect.wav")
except pygame.error as e:
    print(f"Warning: Sound files not found. {e}")
    class DummySound:
        def play(self): pass
    correct_sound = DummySound()
    incorrect_sound = DummySound()

try:
    pygame.mixer.music.load('bgm.ogg')
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except pygame.error as e:
    print(f"Warning: BGM file not found. {e}")

mistake_count = 0
current_trivia_message = None
trivia_display_end_time = 0

POPUP_RECT = None 
POPUP_BG_COLOR = (50, 50, 70) 
POPUP_TEXT_COLOR = (230, 230, 230) 
POPUP_TITLE_COLOR = (250, 250, 150) 
POPUP_LINE_SPACING = 4

def render_text_wrapped(surface, text, font, color, rect, line_spacing=0, antialias=True):
    words = text.split(' ')
    lines = []
    current_line_width = 0
    current_line_text = ""
    for word in words:
        word_surface = font.render(word, antialias, color)
        word_width = word_surface.get_width()
        space_width = font.size(' ')[0]
        if current_line_width + word_width <= rect.width:
            current_line_text += word + " "
            current_line_width += word_width + space_width
        else:
            lines.append(current_line_text.strip())
            current_line_text = word + " "
            current_line_width = word_width + space_width
    lines.append(current_line_text.strip())
    y_offset = rect.top
    for i, line in enumerate(lines):
        if line: 
            line_surface = font.render(line, antialias, color)
            surface.blit(line_surface, (rect.left, y_offset))
            y_offset += font.get_linesize() + line_spacing
            if y_offset > rect.bottom - font.get_linesize():
                break
    return y_offset

def load_chromosome_image(filename, display_id_for_placeholder, width, height):
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (width, height))
    except (pygame.error, FileNotFoundError):
        image = pygame.Surface((width, height))
        image.fill(CHROMOSOME_PLACEHOLDER_BG)
        pygame.draw.rect(image, CHROMOSOME_BORDER_COLOR, image.get_rect(), 1)
        text_surf = placeholder_font.render(display_id_for_placeholder, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(width // 2, height // 2))
        image.blit(text_surf, text_rect)
    return image

def initialize_chromosomes_and_slots(gender):
    global draggable_chromosomes, karyotype_slots, placed_chromosomes_map, mistake_count, current_trivia_message
    global game_start_time, game_state

    draggable_chromosomes.clear()
    karyotype_slots.clear()
    placed_chromosomes_map.clear()
    mistake_count = 0
    current_trivia_message = None
    
    chromosome_filenames_to_load = MALE_CHROMOSOME_FILENAMES if gender == 'male' else FEMALE_CHROMOSOME_FILENAMES
    x_offset = chromosome_list_area_rect.left + 10
    y_offset = chromosome_list_area_rect.top + 40 
    padding = 5
    max_width_in_row = chromosome_list_area_rect.width - 20
    current_x = x_offset
    current_y = y_offset
    for base_filename, id_suffix in chromosome_filenames_to_load:
        full_id_name = f"{gender}_{id_suffix}" 
        img = load_chromosome_image(base_filename, id_suffix, CHROMOSOME_WIDTH, CHROMOSOME_HEIGHT)
        if current_x + CHROMOSOME_WIDTH > x_offset + max_width_in_row:
            current_x = x_offset
            current_y += CHROMOSOME_HEIGHT + padding
        initial_rect = pygame.Rect(current_x, current_y, CHROMOSOME_WIDTH, CHROMOSOME_HEIGHT)
        chromosome = Chromosome(img, full_id_name, initial_rect)
        draggable_chromosomes.append(chromosome)
        current_x += CHROMOSOME_WIDTH + padding

    slot_width = CHROMOSOME_WIDTH + 4
    slot_height = CHROMOSOME_HEIGHT + 4
    slot_padding_horizontal = 10
    slot_padding_vertical = 30 
    pair_padding = 5
    group_padding_horizontal = 40
    num_cols = 6
    start_x = karyotype_template_area_rect.left + 20
    start_y = karyotype_template_area_rect.top + 50
    for i in range(22):
        pair_num = i + 1
        row = i // num_cols
        col = i % num_cols
        slot_pair_base_x = start_x + col * (2 * slot_width + slot_padding_horizontal + pair_padding + group_padding_horizontal / num_cols)
        slot_pair_y = start_y + row * (slot_height + slot_padding_vertical)
        for j, slot_suffix_char in enumerate(["a", "b"]): 
            slot_id = f"{pair_num}{slot_suffix_char}"
            slot_type = str(pair_num) 
            rect_x = slot_pair_base_x + j * (slot_width + pair_padding)
            rect = pygame.Rect(rect_x, slot_pair_y, slot_width, slot_height)
            karyotype_slots.append({'id': slot_id, 'rect': rect, 'occupied_by': None, 'type': slot_type, 'label': str(pair_num)})
    last_autosome_idx = 21 
    row = last_autosome_idx // num_cols
    col = last_autosome_idx % num_cols
    sex_slot_start_x = start_x + (col + 1) * (2 * slot_width + slot_padding_horizontal + pair_padding + group_padding_horizontal / num_cols)
    sex_slot_y = start_y + row * (slot_height + slot_padding_vertical)
    if sex_slot_start_x + 2 * slot_width + pair_padding > karyotype_template_area_rect.right - 20: 
        row += 1
        sex_slot_start_x = start_x 
        sex_slot_y = start_y + row * (slot_height + slot_padding_vertical)
    if gender == 'male':
        sex_slot_definitions = [{'id': "X", 'type': "X", 'label': "X"}, {'id': "Y", 'type': "Y", 'label': "Y"}]
    else: 
        sex_slot_definitions = [{'id': "Xa", 'type': "X", 'label': "X"}, {'id': "Xb", 'type': "X", 'label': "X"}]
    for j, slot_def in enumerate(sex_slot_definitions):
        rect_x = sex_slot_start_x + j * (slot_width + pair_padding)
        rect = pygame.Rect(rect_x, sex_slot_y, slot_width, slot_height)
        karyotype_slots.append({'id': slot_def['id'], 'rect': rect, 'occupied_by': None, 'type': slot_def['type'], 'label': slot_def['label']})
    
    game_state = 'PUZZLE'
    game_start_time = pygame.time.get_ticks()

def draw_chromosome_list_area():
    pygame.draw.rect(screen, PLACEHOLDER_COLOR_1, chromosome_list_area_rect)
    list_label_text = font.render("Chromosomes", True, TEXT_COLOR)
    list_label_rect = list_label_text.get_rect(midtop=(chromosome_list_area_rect.centerx, chromosome_list_area_rect.top + 10))
    screen.blit(list_label_text, list_label_rect)
    for chrom in draggable_chromosomes:
        if not chrom.is_placed and not chrom.is_dragging:
            screen.blit(chrom.image, chrom.current_rect.topleft)

def draw_karyotype_template_area(gender):
    pygame.draw.rect(screen, PLACEHOLDER_COLOR_2, karyotype_template_area_rect)
    gender_specific_title = "Karyotype Template (Male - XY)" if gender == 'male' else "Karyotype Template (Female - XX)"
    karyotype_label_text = font.render(gender_specific_title, True, TEXT_COLOR)
    karyotype_label_rect = karyotype_label_text.get_rect(midtop=(karyotype_template_area_rect.centerx, karyotype_template_area_rect.top + 10))
    screen.blit(karyotype_label_text, karyotype_label_rect)

    # This value is also used in initialize_chromosomes_and_slots.
    # A global constant would be a better solution in a future refactor.
    pair_padding = 5

    for slot in karyotype_slots:
        pygame.draw.rect(screen, CHROMOSOME_BORDER_COLOR, slot['rect'], 2)
        label_text = slot['label'] 
        label_surf = small_font.render(label_text, True, TEXT_COLOR)
        label_pos_x = 0
        draw_this_label = False
        if slot['type'].isdigit(): 
            if slot['id'].endswith('b'): 
                label_pos_x = slot['rect'].left - pair_padding / 2 
                draw_this_label = True
        else: 
            label_pos_x = slot['rect'].centerx
            draw_this_label = True 
        if draw_this_label:
            label_rect = label_surf.get_rect(center=(label_pos_x, slot['rect'].bottom + 10))
            screen.blit(label_surf, label_rect)
        if slot['occupied_by']:
            chrom = slot['occupied_by']
            screen.blit(chrom.image, chrom.current_rect.topleft)

def draw_guessing_ui():
    screen.fill(BACKGROUND_COLOR) # Clear screen or draw over puzzle
    prompt_text = "ぜんぶならべられたね！このDNAは…"
    prompt_surf = font.render(prompt_text, True, TEXT_COLOR)
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(prompt_surf, prompt_rect)

    mouse_pos = pygame.mouse.get_pos()
    # Male button
    male_button_color = BUTTON_HOVER_COLOR if male_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, male_button_color, male_button_rect, border_radius=10)
    male_text_surf = button_font.render("おとこのこ", True, BUTTON_TEXT_COLOR)
    male_text_rect = male_text_surf.get_rect(center=male_button_rect.center)
    screen.blit(male_text_surf, male_text_rect)
    # Female button
    female_button_color = BUTTON_HOVER_COLOR if female_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, female_button_color, female_button_rect, border_radius=10)
    female_text_surf = button_font.render("おんなのこ", True, BUTTON_TEXT_COLOR)
    female_text_rect = female_text_surf.get_rect(center=female_button_rect.center)
    screen.blit(female_text_surf, female_text_rect)

def draw_results_ui():
    screen.fill(BACKGROUND_COLOR)
    
    result_msg_surf = results_font.render(result_message, True, TEXT_COLOR if gender_guess_correct else (200,0,0))
    result_msg_rect = result_msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(result_msg_surf, result_msg_rect)

    score_msg_surf = message_font.render(score_message, True, TEXT_COLOR)
    score_msg_rect = score_msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_msg_surf, score_msg_rect)
    
    actual_gender_msg = f"せいかいは {current_gender.capitalize()} でした。"
    actual_gender_surf = small_font.render(actual_gender_msg, True, TEXT_COLOR)
    actual_gender_rect = actual_gender_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(actual_gender_surf, actual_gender_rect)


# --- Main game loop variables ---
running = True
dragged_chromosome = None
mouse_offset_x = 0
mouse_offset_y = 0

# Define areas 
chromosome_list_area_width = 250 # For POPUP_RECT calculation
chromosome_list_area_x = 20 # For POPUP_RECT calculation
chromosome_list_area_rect = pygame.Rect(chromosome_list_area_x, 20, chromosome_list_area_width, SCREEN_HEIGHT - 40)
karyotype_template_area_rect = pygame.Rect(chromosome_list_area_x + chromosome_list_area_width + 20, 20, SCREEN_WIDTH - (chromosome_list_area_x + chromosome_list_area_width + 20) - 20, SCREEN_HEIGHT - 40)

# Define POPUP_RECT 
POPUP_MARGIN = 20
POPUP_WIDTH = karyotype_template_area_rect.width - (2 * POPUP_MARGIN)
POPUP_HEIGHT = 160 
POPUP_X = karyotype_template_area_rect.left + POPUP_MARGIN
POPUP_Y = karyotype_template_area_rect.bottom - POPUP_HEIGHT - POPUP_MARGIN 
POPUP_RECT = pygame.Rect(POPUP_X, POPUP_Y, POPUP_WIDTH, POPUP_HEIGHT)

# Initial call to set up based on random gender
initialize_chromosomes_and_slots(current_gender) 
pygame.display.set_caption(f"{SCREEN_TITLE} - Sorting {current_gender.capitalize()} Karyotype")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == 'PUZZLE':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    clicked_on_placed_chrom = False
                    if dragged_chromosome is None:
                        for slot in karyotype_slots:
                            if slot['occupied_by'] and slot['rect'].collidepoint(event.pos):
                                dragged_chromosome = slot['occupied_by']
                                slot['occupied_by'] = None 
                                if dragged_chromosome.slot_id in placed_chromosomes_map:
                                    del placed_chromosomes_map[dragged_chromosome.slot_id]
                                dragged_chromosome.is_placed = False
                                dragged_chromosome.is_dragging = True
                                mouse_offset_x = event.pos[0] - dragged_chromosome.current_rect.x
                                mouse_offset_y = event.pos[1] - dragged_chromosome.current_rect.y
                                clicked_on_placed_chrom = True
                                current_trivia_message = None 
                                break
                    if not clicked_on_placed_chrom and dragged_chromosome is None:
                        for chrom in draggable_chromosomes:
                            if not chrom.is_placed and chrom.current_rect.collidepoint(event.pos):
                                dragged_chromosome = chrom
                                dragged_chromosome.is_dragging = True
                                mouse_offset_x = event.pos[0] - chrom.current_rect.x
                                mouse_offset_y = event.pos[1] - chrom.current_rect.y
                                current_trivia_message = None 
                                break 
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragged_chromosome:
                    dropped_on_slot = False
                    for slot in karyotype_slots:
                        if slot['rect'].colliderect(dragged_chromosome.current_rect) and not slot['occupied_by']:
                            dropped_on_slot = True
                            is_correct_placement = (dragged_chromosome.correct_slot_type == slot['type'])
                            if is_correct_placement:
                                dragged_chromosome.current_rect.center = slot['rect'].center
                                dragged_chromosome.is_placed = True
                                dragged_chromosome.slot_id = slot['id']
                                slot['occupied_by'] = dragged_chromosome
                                placed_chromosomes_map[slot['id']] = dragged_chromosome
                                correct_sound.play()
                                chromosome_type_placed = dragged_chromosome.correct_slot_type
                                possible_trivia = [t for t in GENE_LOCI_TRIVIA if t["chromosome_type"] == chromosome_type_placed]
                                if possible_trivia:
                                    current_trivia_message = random.choice(possible_trivia) 
                                    trivia_display_end_time = pygame.time.get_ticks() + TRIVIA_DISPLAY_DURATION
                                else: current_trivia_message = None 
                                
                                # Check for puzzle completion
                                if len(placed_chromosomes_map) == len(karyotype_slots): # All 46 chromosomes placed
                                    puzzle_completion_time = pygame.time.get_ticks()
                                    game_state = 'GUESSING'
                                    current_trivia_message = None # Clear trivia
                            else: 
                                dragged_chromosome.current_rect = dragged_chromosome.original_rect.copy()
                                dragged_chromosome.is_placed = False
                                mistake_count += 1
                                incorrect_sound.play()
                            break 
                    if not dropped_on_slot: 
                        dragged_chromosome.current_rect = dragged_chromosome.original_rect.copy()
                        dragged_chromosome.is_placed = False
                    dragged_chromosome.is_dragging = False
                    dragged_chromosome = None
            elif event.type == pygame.MOUSEMOTION:
                if dragged_chromosome:
                    dragged_chromosome.current_rect.x = event.pos[0] - mouse_offset_x
                    dragged_chromosome.current_rect.y = event.pos[1] - mouse_offset_y
        
        elif game_state == 'GUESSING':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    guessed_gender = None
                    if male_button_rect.collidepoint(event.pos):
                        guessed_gender = 'male'
                    elif female_button_rect.collidepoint(event.pos):
                        guessed_gender = 'female'
                    
                    if guessed_gender:
                        gender_guess_correct = (guessed_gender == current_gender)
                        if gender_guess_correct:
                            result_message = "せいかい！"
                            correct_sound.play()
                        else:
                            result_message = "ざんねん！"
                            incorrect_sound.play()
                        
                        # Calculate Score
                        time_taken_seconds = (puzzle_completion_time - game_start_time) // 1000
                        base_score = 1000
                        mistake_penalty = mistake_count * 10
                        time_penalty = time_taken_seconds * 1 # 1 point per second
                        gender_bonus = 50 if gender_guess_correct else 0
                        final_score = base_score - mistake_penalty - time_penalty + gender_bonus
                        final_score = max(0, final_score) # Ensure score is not negative

                        score_message = f"きみのスコアは {final_score} てん！ DNAはかせに ちかづいたね！"
                        game_state = 'RESULTS'

    # --- Drawing based on Game State ---
    screen.fill(BACKGROUND_COLOR) # Clear screen each frame

    if game_state == 'PUZZLE':
        draw_chromosome_list_area()
        draw_karyotype_template_area(current_gender)
        if dragged_chromosome and dragged_chromosome.is_dragging:
            screen.blit(dragged_chromosome.image, dragged_chromosome.current_rect.topleft)
        
        mistake_text_surf = mistake_font.render(f"Mistakes: {mistake_count}", True, TEXT_COLOR)
        mistake_text_rect = mistake_text_surf.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        screen.blit(mistake_text_surf, mistake_text_rect)
        
        gender_info_surf = small_font.render(f"Gender: {current_gender.capitalize()}", True, TEXT_COLOR) # For testing
        gender_info_rect = gender_info_surf.get_rect(bottomleft=(20, SCREEN_HEIGHT - 20))
        screen.blit(gender_info_surf, gender_info_rect)

        if current_trivia_message and POPUP_RECT: 
            current_time = pygame.time.get_ticks()
            if current_time < trivia_display_end_time:
                pygame.draw.rect(screen, POPUP_BG_COLOR, POPUP_RECT, border_radius=10)
                title_padding = 10; text_padding = 5
                title_rect = pygame.Rect(POPUP_RECT.left + title_padding, POPUP_RECT.top + title_padding, POPUP_RECT.width - (2*title_padding), trivia_font_title.get_linesize())
                render_text_wrapped(screen, current_trivia_message["gene_name"], trivia_font_title, POPUP_TITLE_COLOR, title_rect, 0)
                current_y_offset = title_rect.bottom + text_padding
                explanation_max_height = (POPUP_RECT.height - (current_y_offset - POPUP_RECT.top) - text_padding - trivia_font_text.get_linesize() - text_padding) * 0.6
                explanation_rect = pygame.Rect(POPUP_RECT.left + title_padding, current_y_offset, POPUP_RECT.width - (2*title_padding), explanation_max_height)
                last_y_explanation = render_text_wrapped(screen, "説明: " + current_trivia_message["explanation"], trivia_font_text, POPUP_TEXT_COLOR, explanation_rect, POPUP_LINE_SPACING)
                current_y_offset = last_y_explanation 
                if current_y_offset < explanation_rect.bottom : current_y_offset = explanation_rect.bottom
                current_y_offset += text_padding 
                trait_max_height = POPUP_RECT.bottom - current_y_offset - title_padding 
                trait_rect = pygame.Rect(POPUP_RECT.left + title_padding, current_y_offset, POPUP_RECT.width - (2*title_padding), trait_max_height)
                render_text_wrapped(screen, "形質: " + current_trivia_message["trait"], trivia_font_text, POPUP_TEXT_COLOR, trait_rect, POPUP_LINE_SPACING)
            else: current_trivia_message = None 
    
    elif game_state == 'GUESSING':
        draw_guessing_ui()

    elif game_state == 'RESULTS':
        draw_results_ui()

    pygame.display.flip()

pygame.quit()
