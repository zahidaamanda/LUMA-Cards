import sqlite3
import os
import shutil
from pathlib import Path
import sys

class UserDatabase:
    def __init__(self, db_name='users.db'):
        """Inisialisasi database"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
        # Dapatkan base directory aplikasi
        if getattr(sys, 'frozen', False):
            # Jika di-compile menjadi executable
            self.base_dir = Path(sys.executable).parent
        else:
            # Jika berjalan sebagai script Python
            self.base_dir = Path(__file__).parent
        
        print(f"Base directory: {self.base_dir}")
        self.init_database()
    
    def get_app_path(self, *paths):
        """Mendapatkan path absolut di dalam folder aplikasi"""
        return str(self.base_dir.joinpath(*paths))
    
    def connect(self):
        """Membuat koneksi ke database"""
        db_path = self.get_app_path(self.db_name)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
    
    def close(self):
        """Menutup koneksi database"""
        if self.connection:
            self.connection.close()
    
    def init_database(self):
        """Membuat tabel jika belum ada"""
        self.connect()
        
        # Buat tabel users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                no_id TEXT,
                division TEXT,
                birth_date TEXT,
                email TEXT,
                photo_path TEXT,
                signup_complete INTEGER DEFAULT 0,
                biodata_complete INTEGER DEFAULT 0,
                photo_complete INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
        self.close()
    
    def create_user(self, username, password):
        """Membuat user baru (signup)"""
        try:
            self.connect()
            self.cursor.execute('''
                INSERT INTO users (username, password, signup_complete)
                VALUES (?, ?, 1)
            ''', (username, password))
            user_id = self.cursor.lastrowid
            self.connection.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None  # Username sudah ada
        finally:
            self.close()
    
    def update_biodata(self, username, full_name, no_id, division, birth_date, email):
        """Update data biodata user"""
        try:
            self.connect()
            self.cursor.execute('''
                UPDATE users 
                SET full_name = ?, no_id = ?, division = ?, 
                    birth_date = ?, email = ?, biodata_complete = 1
                WHERE username = ?
            ''', (full_name, no_id, division, birth_date, email, username))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating biodata: {e}")
            return False
        finally:
            self.close()
    
    def update_photo(self, username, photo_path):
        """Update foto user dan copy ke folder aplikasi"""
        try:
            # Buat folder untuk menyimpan foto di dalam aplikasi
            photos_dir = self.base_dir / "user_photos"
            photos_dir.mkdir(exist_ok=True)
            
            print(f"Source photo path: {photo_path}")
            print(f"Photos directory: {photos_dir}")
            
            # Pastikan file sumber ada
            if not os.path.exists(photo_path):
                print(f"Source file does not exist: {photo_path}")
                return None
            
            # Generate nama file unik
            import uuid
            file_ext = Path(photo_path).suffix.lower()
            new_filename = f"{username}_{uuid.uuid4().hex[:8]}{file_ext}"
            new_path = photos_dir / new_filename
            
            print(f"New photo path: {new_path}")
            
            # Copy file ke folder aplikasi
            shutil.copy2(photo_path, str(new_path))
            
            # Verifikasi file berhasil disalin
            if not os.path.exists(str(new_path)):
                print(f"Failed to copy file to: {new_path}")
                return None
            
            # Simpan path RELATIF ke database (relative to base_dir)
            # Ini lebih portable
            relative_path = f"user_photos/{new_filename}"
            
            # Update database
            self.connect()
            self.cursor.execute('''
                UPDATE users 
                SET photo_path = ?, photo_complete = 1
                WHERE username = ?
            ''', (relative_path, username))
            self.connection.commit()
            
            print(f"Photo saved to: {relative_path}")
            return relative_path
        except Exception as e:
            print(f"Error updating photo: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            self.close()
    
    def complete_registration(self, username):
        """Tandai registrasi selesai"""
        try:
            self.connect()
            self.cursor.execute('''
                UPDATE users 
                SET signup_complete = 1, biodata_complete = 1, photo_complete = 1
                WHERE username = ?
            ''', (username,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error completing registration: {e}")
            return False
        finally:
            self.close()
    
    def verify_login(self, username, password):
        """Verifikasi login"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT id, username FROM users 
                WHERE username = ? AND password = ?
            ''', (username, password))
            user = self.cursor.fetchone()
            return user  # Return (id, username) jika berhasil
        except Exception as e:
            print(f"Error verifying login: {e}")
            return None
        finally:
            self.close()
    
    def get_user_data(self, username):
        """Mendapatkan semua data user untuk ditampilkan di card"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT full_name, no_id, division, birth_date, email, photo_path
                FROM users 
                WHERE username = ?
            ''', (username,))
            user_data = self.cursor.fetchone()
            
            if user_data and user_data[5]:  # photo_path di index 5
                # Konversi path relatif ke path absolut
                photo_path = user_data[5]
                absolute_photo_path = self.get_app_path(photo_path)
                
                # Periksa apakah file ada
                if os.path.exists(absolute_photo_path):
                    print(f"Photo found: {absolute_photo_path}")
                    # Return tuple dengan path absolut
                    return (*user_data[:5], absolute_photo_path)
                else:
                    print(f"Photo not found: {absolute_photo_path}")
                    # Return tanpa photo_path
                    return (*user_data[:5], None)
            
            return user_data
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
        finally:
            self.close()
    
    def check_username_exists(self, username):
        """Cek apakah username sudah terdaftar"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT id FROM users WHERE username = ?
            ''', (username,))
            return self.cursor.fetchone() is not None
        finally:
            self.close()
    
    def get_user_progress(self, username):
        """Mendapatkan progress registrasi user"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT signup_complete, biodata_complete, photo_complete 
                FROM users WHERE username = ?
            ''', (username,))
            return self.cursor.fetchone()
        finally:
            self.close()