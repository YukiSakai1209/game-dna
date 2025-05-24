import os

import pygame

print(f"Pygame version: {pygame.version.ver if hasattr(pygame, 'version') else 'N/A'}")
if hasattr(pygame, "get_sdl_version"):
    sdl_major, sdl_minor, sdl_patch = pygame.get_sdl_version()
    print(f"SDL version: {sdl_major}.{sdl_minor}.{sdl_patch}")


class DummySound:
    def __init__(self, filename=""):
        self.filename = filename
        print(f"DummySound initialized for: {filename if filename else 'generic'}")

    def play(self):
        print(f"DummySound.play() called for: {self.filename if filename else 'generic'}")


print("Attempting pygame.mixer.init()...")
try:
    pygame.mixer.init()  # Try with default settings
    print("pygame.mixer.init() successful.")
except pygame.error as e:
    print(f"ERROR during pygame.mixer.init(): {e}")
    print("Attempting pygame.mixer.pre_init() with different settings...")
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Retry with common settings
        pygame.mixer.init()
        print("pygame.mixer.init() successful after pre_init.")
    except pygame.error as e2:
        print(f"ERROR during pygame.mixer.init() even after pre_init: {e2}")
        print("Sound tests cannot proceed. Please check your audio system and Pygame/SDL installation.")
        pygame.quit()
        exit()  # Exit the script if mixer cannot be initialized
except Exception as e_init_unexpected:
    print(
        f"UNEXPECTED ERROR during pygame.mixer.init(): {type(e_init_unexpected).__name__} - {e_init_unexpected}"
    )
    print("Sound tests cannot proceed.")
    pygame.quit()
    exit()  # Exit the script if mixer cannot be initialized

sound_filename = "a_sound_file_that_does_not_exist.wav"  # Intentionally non-existent

print(f"Current working directory: {os.getcwd()}")
target_file_path = os.path.join(os.getcwd(), sound_filename)
print(f"Attempting to load sound file: {target_file_path}")
print(f"Does the target file exist? {os.path.exists(target_file_path)}")

sound_object = None  # Initialize variable
try:
    sound_object = pygame.mixer.Sound(sound_filename)
    print(
        f"SUCCESS: pygame.mixer.Sound('{sound_filename}') loaded the sound. (This should NOT happen if the file is truly missing or inaccessible)"
    )
    if sound_object:
        print(f"Playing actual sound: {sound_filename}")
        sound_object.play()
except FileNotFoundError as e_fnf:
    print(f"CAUGHT FileNotFoundError: Could not load {sound_filename}. Error details: {e_fnf}")
    print("Assigning DummySound due to FileNotFoundError.")
    sound_object = DummySound(sound_filename)
    if sound_object:
        sound_object.play()
except (
    pygame.error
) as e_pygame:  # Other Pygame errors (like SDL errors, sometimes file not found also comes here)
    print(f"CAUGHT pygame.error: Could not load {sound_filename}. Error details: {e_pygame}")
    print("Assigning DummySound due to pygame.error.")
    sound_object = DummySound(sound_filename)
    if sound_object:
        sound_object.play()
except Exception as e_unexpected:  # Other unexpected errors
    print(
        f"CAUGHT UNEXPECTED ERROR: Could not load {sound_filename}. Error type: {type(e_unexpected).__name__}, Details: {e_unexpected}"
    )
    print("Assigning DummySound due to unexpected error.")
    sound_object = DummySound(sound_filename)
    if sound_object:
        sound_object.play()

print("-" * 30)  # Separator line
if isinstance(sound_object, DummySound):
    print("Final Test Result: DummySound was correctly assigned.")
elif sound_object is not None:
    print("Final Test Result: Real sound object exists. (This is unexpected if the sound file was missing).")
else:
    print(
        "Final Test Result: sound_object is None. (Loading failed, and DummySound was not assigned - check logic)."
    )

print("Sound test script finished.")
pygame.quit()  # Quit Pygame
