from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Import database
from database import UserDatabase

# Import semua screen
from hal_welcome import HalWelcome
from hal_login import HalLogin
from hal_signup import HalSignup
from hal_biodata import HalBiodata
from hal_poto import HalPoto
from hal_card import HalCard

class LUMACard(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inisialisasi database
        self.db = UserDatabase()
    
    def build(self):
        # Fixed window size
        Window.size = (1366, 768)
        Window.resizable = False
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        # Buat ScreenManager
        sm = ScreenManager(transition=FadeTransition(duration=0.5))
        
        # Tambahkan screens
        sm.add_widget(HalWelcome())
        sm.add_widget(HalLogin())
        sm.add_widget(HalSignup())
        sm.add_widget(HalBiodata())
        sm.add_widget(HalPoto())
        sm.add_widget(HalCard())

        return sm

if __name__ == '__main__':
    LUMACard().run()   