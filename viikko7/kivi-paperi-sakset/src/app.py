from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luo_peli import LuoPeli
from tuomari import Tuomari

app = Flask(__name__)
app.secret_key = 'kivi-paperi-sakset-secret-key-2025'


@app.route('/')
def index():
    """Main menu page"""
    session.clear()
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_game():
    """Initialize a new game"""
    game_type = request.form.get('game_type')
    peli = LuoPeli.luo_peli(game_type)
    
    if peli is None:
        return redirect(url_for('index'))
    
    # Initialize game state in session
    session['game_type'] = game_type
    session['tuomari'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    }
    session['round'] = 1
    session['last_result'] = None
    session['game_over'] = False
    
    # Store AI state for non-PvP games
    if game_type == 'b':
        session['ai_siirto'] = 0
    elif game_type == 'c':
        session['ai_muisti'] = [None] * 10
        session['ai_vapaa_indeksi'] = 0
    
    return redirect(url_for('play'))


@app.route('/play')
def play():
    """Game play page"""
    if 'game_type' not in session:
        return redirect(url_for('index'))
    
    if session.get('game_over'):
        return redirect(url_for('game_over'))
    
    game_type = session['game_type']
    tuomari_data = session['tuomari']
    round_num = session.get('round', 1)
    last_result = session.get('last_result')
    
    # Determine game mode name
    game_modes = {
        'a': 'Pelaaja vs Pelaaja',
        'b': 'Pelaaja vs Tekoäly',
        'c': 'Pelaaja vs Parannettu Tekoäly'
    }
    game_mode = game_modes.get(game_type, 'Tuntematon')
    
    return render_template('play.html', 
                         game_type=game_type,
                         game_mode=game_mode,
                         tuomari=tuomari_data,
                         round=round_num,
                         last_result=last_result)


@app.route('/move', methods=['POST'])
def make_move():
    """Process a move"""
    if 'game_type' not in session or session.get('game_over'):
        return redirect(url_for('index'))
    
    ekan_siirto = request.form.get('ekan_siirto')
    game_type = session['game_type']
    
    # Validate move
    if ekan_siirto not in ['k', 'p', 's']:
        return redirect(url_for('play'))
    
    # Get second player's move
    if game_type == 'a':
        # Player vs Player
        tokan_siirto = request.form.get('tokan_siirto')
        if tokan_siirto not in ['k', 'p', 's']:
            return redirect(url_for('play'))
    elif game_type == 'b':
        # Simple AI
        tokan_siirto = _simple_ai_move()
    else:  # game_type == 'c'
        # Advanced AI
        tokan_siirto = _advanced_ai_move(ekan_siirto)
    
    # Create tuomari and update scores
    tuomari = Tuomari()
    tuomari.ekan_pisteet = session['tuomari']['ekan_pisteet']
    tuomari.tokan_pisteet = session['tuomari']['tokan_pisteet']
    tuomari.tasapelit = session['tuomari']['tasapelit']
    
    tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
    
    # Update session
    session['tuomari'] = {
        'ekan_pisteet': tuomari.ekan_pisteet,
        'tokan_pisteet': tuomari.tokan_pisteet,
        'tasapelit': tuomari.tasapelit
    }
    
    # Determine round result
    move_names = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    if ekan_siirto == tokan_siirto:
        result = 'Tasapeli!'
    elif tuomari._eka_voittaa(ekan_siirto, tokan_siirto):
        result = 'Pelaaja 1 voitti kierroksen!'
    else:
        result = 'Pelaaja 2 voitti kierroksen!'
    
    session['last_result'] = {
        'ekan_siirto': move_names[ekan_siirto],
        'tokan_siirto': move_names[tokan_siirto],
        'result': result
    }
    
    session['round'] = session.get('round', 1) + 1
    
    # Check if game is over (3 wins)
    if tuomari.peli_ohi(3):
        session['game_over'] = True
        return redirect(url_for('game_over'))
    
    return redirect(url_for('play'))


@app.route('/game_over')
def game_over():
    """Game over page"""
    if 'tuomari' not in session:
        return redirect(url_for('index'))
    
    tuomari_data = session['tuomari']
    game_type = session.get('game_type')
    
    # Determine winner
    if tuomari_data['ekan_pisteet'] >= 3:
        winner = 'Pelaaja 1 voitti pelin!'
    elif tuomari_data['tokan_pisteet'] >= 3:
        if game_type == 'a':
            winner = 'Pelaaja 2 voitti pelin!'
        else:
            winner = 'Tietokone voitti pelin!'
    else:
        winner = 'Peli keskeytetty'
    
    return render_template('game_over.html', 
                         tuomari=tuomari_data,
                         winner=winner)


def _simple_ai_move():
    """Simple AI that cycles through moves"""
    siirto = session.get('ai_siirto', 0)
    siirto = (siirto + 1) % 3
    session['ai_siirto'] = siirto
    
    if siirto == 0:
        return 'k'
    elif siirto == 1:
        return 'p'
    else:
        return 's'


def _advanced_ai_move(ekan_siirto):
    """Advanced AI that learns from player's patterns"""
    muisti = session.get('ai_muisti', [None] * 10)
    vapaa_indeksi = session.get('ai_vapaa_indeksi', 0)
    
    # Determine AI move based on memory
    if vapaa_indeksi in [0, 1]:
        ai_move = 'k'
    else:
        viimeisin_siirto = muisti[vapaa_indeksi - 1]
        k, p, s = 0, 0, 0
        
        for i in range(0, vapaa_indeksi - 1):
            if viimeisin_siirto == muisti[i]:
                seuraava = muisti[i + 1]
                if seuraava == 'k':
                    k += 1
                elif seuraava == 'p':
                    p += 1
                else:
                    s += 1
        
        if k > p or k > s:
            ai_move = 'p'
        elif p > k or p > s:
            ai_move = 's'
        else:
            ai_move = 'k'
    
    # Store player's move in memory
    if vapaa_indeksi == len(muisti):
        # Shift memory
        for i in range(1, len(muisti)):
            muisti[i - 1] = muisti[i]
        vapaa_indeksi -= 1
    
    muisti[vapaa_indeksi] = ekan_siirto
    vapaa_indeksi += 1
    
    session['ai_muisti'] = muisti
    session['ai_vapaa_indeksi'] = vapaa_indeksi
    
    return ai_move


if __name__ == '__main__':
    app.run(debug=True, port=5000)
