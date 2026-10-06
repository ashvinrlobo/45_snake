import math
import struct
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 2)
            self.enabled = True
        except Exception as e:
            print("Sound initialization failed:", e)

        self.eat_sound = None
        self.game_over_sound = None

        if self.enabled:
            self._create_sounds()

    def _create_sounds(self):
        try:
            self.eat_sound = self._generate_eat_sound()
            self.game_over_sound = self._generate_game_over_sound()
        except Exception as e:
            print("Sound creation failed:", e)

    def _generate_eat_sound(self):
        # A pleasant dual-tone arpeggio (E5 -> B5, 0.12s total)
        sample_rate = 44100
        duration = 0.12
        num_samples = int(sample_rate * duration)
        buf = bytearray()
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Frequency steps from 659Hz to 987Hz halfway through
            freq = 659.25 if t < 0.06 else 987.77
            # Fade out envelope
            env = 1.0 - (t / duration)
            val = int(32767.0 * 0.25 * env * math.sin(2.0 * math.pi * freq * t))
            buf.extend(struct.pack("<hh", val, val))
            
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generate_game_over_sound(self):
        # Descending buzz (350Hz down to 100Hz, 0.4s)
        sample_rate = 44100
        duration = 0.4
        num_samples = int(sample_rate * duration)
        buf = bytearray()
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Frequency slides down from 350 to 100
            freq = 350.0 - (250.0 * (t / duration))
            # Envelope with decay
            env = max(0.0, 1.0 - (t / duration))
            # Sine + square mixture for classic arcade sound
            sine_wave = math.sin(2.0 * math.pi * freq * t)
            sq_wave = 0.5 if sine_wave > 0 else -0.5
            mix = (0.7 * sine_wave) + (0.3 * sq_wave)
            
            val = int(32767.0 * 0.3 * env * mix)
            buf.extend(struct.pack("<hh", val, val))
            
        return pygame.mixer.Sound(buffer=bytes(buf))

    def play_eat(self):
        if self.enabled and self.eat_sound:
            try:
                self.eat_sound.play()
            except Exception:
                pass

    def play_game_over(self):
        if self.enabled and self.game_over_sound:
            try:
                self.game_over_sound.play()
            except Exception:
                pass
