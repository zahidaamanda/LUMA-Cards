from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder

KV_WELCOME = '''
<HalWelcome>:
    FloatLayout:
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        Image:
            source: 'Media/Logo hal 1.png'
            size_hint: None, None
            size: 1366, 768
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
'''

Builder.load_string(KV_WELCOME)

class HalWelcome(Screen):
    """Screen untuk gambar pertama (Logo hal 1)"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'welcome'
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        # Setelah 5 detik, pindah ke screen login
        Clock.schedule_once(self.go_to_login, 5)
    
    def go_to_login(self, dt):
        """Pindah ke screen login"""
        if self.manager:
            self.manager.current = 'login'