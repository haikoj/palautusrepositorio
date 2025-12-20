"""
Tests for the existing game logic classes
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from luo_peli import LuoPeli
from kivi_paperi_sakset import KiviPaperiSakset
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


class TestTuomari:
    """Test the Tuomari (referee) class"""
    
    def test_tuomari_initialization(self):
        """Test tuomari starts with zero scores"""
        tuomari = Tuomari()
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
    
    def test_kirjaa_siirto_tasapeli(self):
        """Test recording a tie"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('k', 'k')
        assert tuomari.tasapelit == 1
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
    
    def test_kirjaa_siirto_eka_voittaa_kivi_sakset(self):
        """Test first player wins with rock vs scissors"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('k', 's')
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
    
    def test_kirjaa_siirto_eka_voittaa_sakset_paperi(self):
        """Test first player wins with scissors vs paper"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('s', 'p')
        assert tuomari.ekan_pisteet == 1
    
    def test_kirjaa_siirto_eka_voittaa_paperi_kivi(self):
        """Test first player wins with paper vs rock"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('p', 'k')
        assert tuomari.ekan_pisteet == 1
    
    def test_kirjaa_siirto_toka_voittaa(self):
        """Test second player wins"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('k', 'p')
        assert tuomari.tokan_pisteet == 1
        assert tuomari.ekan_pisteet == 0
    
    def test_peli_ohi_eka_voittaa(self):
        """Test game ends when first player reaches 5 wins"""
        tuomari = Tuomari()
        for _ in range(5):
            tuomari.kirjaa_siirto('k', 's')
        assert tuomari.peli_ohi(5) is True
    
    def test_peli_ohi_toka_voittaa(self):
        """Test game ends when second player reaches 5 wins"""
        tuomari = Tuomari()
        for _ in range(5):
            tuomari.kirjaa_siirto('s', 'k')
        assert tuomari.peli_ohi(5) is True
    
    def test_peli_ohi_not_yet(self):
        """Test game continues when neither player has 5 wins"""
        tuomari = Tuomari()
        for _ in range(4):
            tuomari.kirjaa_siirto('k', 's')
        assert tuomari.peli_ohi(5) is False
    
    def test_peli_ohi_custom_limit(self):
        """Test game with custom win limit"""
        tuomari = Tuomari()
        for _ in range(3):
            tuomari.kirjaa_siirto('k', 's')
        assert tuomari.peli_ohi(3) is True
        assert tuomari.peli_ohi(5) is False
    
    def test_str_representation(self):
        """Test string representation of tuomari"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto('k', 's')
        tuomari.kirjaa_siirto('k', 'k')
        result = str(tuomari)
        assert '1 - 0' in result
        assert 'Tasapelit: 1' in result


class TestTekoaly:
    """Test the simple AI class"""
    
    def test_tekoaly_initialization(self):
        """Test AI initializes with siirto=0"""
        ai = Tekoaly()
        assert ai._siirto == 0
    
    def test_tekoaly_cycles_correctly(self):
        """Test AI cycles through k, p, s"""
        ai = Tekoaly()
        
        # First call: 0+1 % 3 = 1 -> 'p'
        assert ai.anna_siirto() == 'p'
        
        # Second call: 1+1 % 3 = 2 -> 's'
        assert ai.anna_siirto() == 's'
        
        # Third call: 2+1 % 3 = 0 -> 'k'
        assert ai.anna_siirto() == 'k'
        
        # Fourth call: 0+1 % 3 = 1 -> 'p'
        assert ai.anna_siirto() == 'p'
    
    def test_tekoaly_sequence(self):
        """Test AI produces expected sequence"""
        ai = Tekoaly()
        moves = [ai.anna_siirto() for _ in range(6)]
        assert moves == ['p', 's', 'k', 'p', 's', 'k']


class TestTekoalyParannettu:
    """Test the advanced AI class"""
    
    def test_tekoaly_parannettu_initialization(self):
        """Test advanced AI initializes correctly"""
        ai = TekoalyParannettu(10)
        assert len(ai._muisti) == 10
        assert ai._vapaa_muisti_indeksi == 0
    
    def test_anna_siirto_empty_memory(self):
        """Test AI returns 'k' when memory is empty"""
        ai = TekoalyParannettu(10)
        assert ai.anna_siirto() == 'k'
    
    def test_anna_siirto_one_move_in_memory(self):
        """Test AI returns 'k' when only one move in memory"""
        ai = TekoalyParannettu(10)
        ai.aseta_siirto('k')
        assert ai.anna_siirto() == 'k'
    
    def test_aseta_siirto_stores_move(self):
        """Test setting a move stores it in memory"""
        ai = TekoalyParannettu(10)
        ai.aseta_siirto('k')
        assert ai._muisti[0] == 'k'
        assert ai._vapaa_muisti_indeksi == 1
    
    def test_aseta_siirto_multiple_moves(self):
        """Test storing multiple moves"""
        ai = TekoalyParannettu(5)
        moves = ['k', 'p', 's', 'k', 'p']
        for move in moves:
            ai.aseta_siirto(move)
        assert ai._muisti[:5] == moves
        assert ai._vapaa_muisti_indeksi == 5
    
    def test_anna_siirto_pattern_detection(self):
        """Test AI detects patterns and predicts"""
        ai = TekoalyParannettu(10)
        
        # Create pattern: after 'k', player always plays 'p'
        ai.aseta_siirto('k')
        ai.aseta_siirto('p')
        ai.aseta_siirto('k')
        ai.aseta_siirto('p')
        ai.aseta_siirto('k')
        
        # AI should predict 'p' and counter with 's'
        move = ai.anna_siirto()
        assert move == 's'  # Counters expected 'p'


class TestLuoPeli:
    """Test the factory class for creating games"""
    
    def test_luo_peli_type_a(self):
        """Test creating player vs player game"""
        peli = LuoPeli.luo_peli('a')
        assert isinstance(peli, KPSPelaajaVsPelaaja)
    
    def test_luo_peli_type_b(self):
        """Test creating game with simple AI"""
        peli = LuoPeli.luo_peli('b')
        assert isinstance(peli, KPSTekoaly)
    
    def test_luo_peli_type_c(self):
        """Test creating game with advanced AI"""
        peli = LuoPeli.luo_peli('c')
        assert isinstance(peli, KPSParempiTekoaly)
    
    def test_luo_peli_invalid_type(self):
        """Test invalid game type returns None"""
        peli = LuoPeli.luo_peli('x')
        assert peli is None
    
    def test_luo_peli_none_type(self):
        """Test None type returns None"""
        peli = LuoPeli.luo_peli(None)
        assert peli is None


class TestKiviPaperiSakset:
    """Test the base game class"""
    
    def test_onko_ok_siirto_valid_moves(self):
        """Test valid move detection"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto('k') is True
        assert peli._onko_ok_siirto('p') is True
        assert peli._onko_ok_siirto('s') is True
    
    def test_onko_ok_siirto_invalid_moves(self):
        """Test invalid move detection"""
        peli = KiviPaperiSakset()
        assert peli._onko_ok_siirto('x') is False
        assert peli._onko_ok_siirto('') is False
        assert peli._onko_ok_siirto('kivi') is False
        assert peli._onko_ok_siirto('K') is False


class TestKPSPelaajaVsPelaaja:
    """Test player vs player game class"""
    
    def test_inheritance(self):
        """Test that KPSPelaajaVsPelaaja inherits from KiviPaperiSakset"""
        peli = KPSPelaajaVsPelaaja()
        assert isinstance(peli, KiviPaperiSakset)
    
    def test_toisen_siirto_method_exists(self):
        """Test that _toisen_siirto method exists"""
        peli = KPSPelaajaVsPelaaja()
        assert hasattr(peli, '_toisen_siirto')


class TestKPSTekoaly:
    """Test game with simple AI"""
    
    def test_initialization(self):
        """Test KPSTekoaly initializes with AI"""
        peli = KPSTekoaly()
        assert hasattr(peli, 'tekoaly')
        assert isinstance(peli.tekoaly, Tekoaly)
    
    def test_inheritance(self):
        """Test that KPSTekoaly inherits from KiviPaperiSakset"""
        peli = KPSTekoaly()
        assert isinstance(peli, KiviPaperiSakset)


class TestKPSParempiTekoaly:
    """Test game with advanced AI"""
    
    def test_initialization(self):
        """Test KPSParempiTekoaly initializes with advanced AI"""
        peli = KPSParempiTekoaly()
        assert hasattr(peli, 'supertekoaly')
        assert isinstance(peli.supertekoaly, TekoalyParannettu)
    
    def test_inheritance(self):
        """Test that KPSParempiTekoaly inherits from KiviPaperiSakset"""
        peli = KPSParempiTekoaly()
        assert isinstance(peli, KiviPaperiSakset)
    
    def test_ai_memory_size(self):
        """Test AI is initialized with correct memory size"""
        peli = KPSParempiTekoaly()
        assert len(peli.supertekoaly._muisti) == 10
