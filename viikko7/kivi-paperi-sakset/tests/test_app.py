import pytest
from flask import session


class TestRoutes:
    """Test all Flask routes"""
    
    def test_index_route(self, client):
        """Test the main index page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data
        assert b'Valitse pelimuoto' in response.data
    
    def test_index_clears_session(self, client):
        """Test that visiting index clears the session"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['round'] = 5
        
        client.get('/')
        
        with client.session_transaction() as sess:
            assert 'game_type' not in sess
            assert 'round' not in sess


class TestStartGame:
    """Test game initialization"""
    
    def test_start_game_type_a(self, client):
        """Test starting player vs player game"""
        response = client.post('/start', data={'game_type': 'a'}, follow_redirects=False)
        assert response.status_code == 302
        assert '/play' in response.location
        
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'a'
            assert sess['tuomari']['ekan_pisteet'] == 0
            assert sess['tuomari']['tokan_pisteet'] == 0
            assert sess['tuomari']['tasapelit'] == 0
            assert sess['round'] == 1
            assert sess['game_over'] is False
            assert 'ai_siirto' not in sess
            assert 'ai_muisti' not in sess
    
    def test_start_game_type_b(self, client):
        """Test starting game with simple AI"""
        response = client.post('/start', data={'game_type': 'b'}, follow_redirects=False)
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'b'
            assert sess['ai_siirto'] == 0
            assert 'ai_muisti' not in sess
    
    def test_start_game_type_c(self, client):
        """Test starting game with advanced AI"""
        response = client.post('/start', data={'game_type': 'c'}, follow_redirects=False)
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['game_type'] == 'c'
            assert sess['ai_muisti'] == [None] * 10
            assert sess['ai_vapaa_indeksi'] == 0
            assert 'ai_siirto' not in sess
    
    def test_start_game_invalid_type(self, client):
        """Test starting game with invalid type redirects to index"""
        response = client.post('/start', data={'game_type': 'x'}, follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_start_game_no_type(self, client):
        """Test starting game without type"""
        response = client.post('/start', data={}, follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location


class TestPlayRoute:
    """Test the play route"""
    
    def test_play_without_game_redirects(self, client):
        """Test accessing play without starting a game"""
        response = client.get('/play', follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_play_with_game_type_a(self, client):
        """Test play page for player vs player"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 1, 'tokan_pisteet': 2, 'tasapelit': 1}
            sess['round'] = 3
            sess['game_over'] = False
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'Pelaaja vs Pelaaja' in response.data
        assert b'Kierros: 3' in response.data
    
    def test_play_with_game_type_b(self, client):
        """Test play page for AI game"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'b'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_siirto'] = 0
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'vs' in response.data
    
    def test_play_with_last_result(self, client):
        """Test play page shows last result"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 1, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 2
            sess['game_over'] = False
            sess['last_result'] = {
                'ekan_siirto': 'Kivi',
                'tokan_siirto': 'Sakset',
                'result': 'Pelaaja 1 voitti kierroksen!'
            }
        
        response = client.get('/play')
        assert response.status_code == 200
        assert b'Edellinen kierros' in response.data
        assert b'Kivi' in response.data
        assert b'Sakset' in response.data
    
    def test_play_when_game_over_redirects(self, client):
        """Test play redirects to game_over when game is finished"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 3, 'tasapelit': 0}
            sess['game_over'] = True
        
        response = client.get('/play', follow_redirects=False)
        assert response.status_code == 302
        assert '/game_over' in response.location


class TestMakeMove:
    """Test making moves in the game"""
    
    def test_make_move_without_game(self, client):
        """Test making a move without starting a game"""
        response = client.post('/move', data={'ekan_siirto': 'k'}, follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_make_move_when_game_over(self, client):
        """Test making a move when game is already over"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['game_over'] = True
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'p'}, 
                              follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_make_move_invalid_first_move(self, client):
        """Test with invalid first player move"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'x', 'tokan_siirto': 'k'}, 
                              follow_redirects=False)
        assert response.status_code == 302
        assert '/play' in response.location
    
    def test_make_move_pvp_tie(self, client):
        """Test player vs player with a tie"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'k'}, 
                              follow_redirects=False)
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['tasapelit'] == 1
            assert sess['tuomari']['ekan_pisteet'] == 0
            assert sess['tuomari']['tokan_pisteet'] == 0
            assert sess['round'] == 2
            assert 'Tasapeli' in sess['last_result']['result']
    
    def test_make_move_pvp_player1_wins(self, client):
        """Test player 1 winning a round"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 's'}, 
                              follow_redirects=False)
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['ekan_pisteet'] == 1
            assert sess['tuomari']['tokan_pisteet'] == 0
            assert 'Pelaaja 1 voitti' in sess['last_result']['result']
    
    def test_make_move_pvp_player2_wins(self, client):
        """Test player 2 winning a round"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'p'}, 
                              follow_redirects=False)
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['tokan_pisteet'] == 1
            assert sess['tuomari']['ekan_pisteet'] == 0
            assert 'Pelaaja 2 voitti' in sess['last_result']['result']
    
    def test_make_move_pvp_invalid_second_move(self, client):
        """Test with invalid second player move"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'invalid'}, 
                              follow_redirects=False)
        assert response.status_code == 302
        assert '/play' in response.location
    
    def test_make_move_simple_ai(self, client):
        """Test making a move against simple AI"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'b'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_siirto'] = 0
        
        response = client.post('/move', data={'ekan_siirto': 'k'}, follow_redirects=False)
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['ai_siirto'] == 1  # AI cycles through moves
            assert sess['round'] == 2
    
    def test_make_move_advanced_ai(self, client):
        """Test making a move against advanced AI"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'c'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_muisti'] = [None] * 10
            sess['ai_vapaa_indeksi'] = 0
        
        response = client.post('/move', data={'ekan_siirto': 'p'}, follow_redirects=False)
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['ai_muisti'][0] == 'p'  # Player move stored
            assert sess['ai_vapaa_indeksi'] == 1
            assert sess['round'] == 2
    
    def test_make_move_game_ends_at_5_wins_player1(self, client):
        """Test game ends when player 1 reaches 5 wins"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 4, 'tokan_pisteet': 2, 'tasapelit': 0}
            sess['round'] = 7
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 's'}, 
                              follow_redirects=False)
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['ekan_pisteet'] == 5
            assert sess['game_over'] is True
        
        assert '/game_over' in response.location
    
    def test_make_move_game_ends_at_5_wins_player2(self, client):
        """Test game ends when player 2 reaches 5 wins"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 1, 'tokan_pisteet': 4, 'tasapelit': 0}
            sess['round'] = 6
            sess['game_over'] = False
        
        response = client.post('/move', data={'ekan_siirto': 's', 'tokan_siirto': 'k'}, 
                              follow_redirects=False)
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['tokan_pisteet'] == 5
            assert sess['game_over'] is True
        
        assert '/game_over' in response.location
    
    def test_move_names_conversion(self, client):
        """Test that move codes are converted to Finnish names"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'p'})
        
        with client.session_transaction() as sess:
            assert sess['last_result']['ekan_siirto'] == 'Kivi'
            assert sess['last_result']['tokan_siirto'] == 'Paperi'


class TestGameOver:
    """Test game over page"""
    
    def test_game_over_without_game(self, client):
        """Test accessing game_over without a game"""
        response = client.get('/game_over', follow_redirects=False)
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_game_over_player1_wins(self, client):
        """Test game over page when player 1 wins"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 5, 'tokan_pisteet': 3, 'tasapelit': 2}
        
        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'Pelaaja 1 voitti pelin!' in response.data
        assert b'5 - 3' in response.data
        assert b'Tasapelit: 2' in response.data
    
    def test_game_over_player2_wins_pvp(self, client):
        """Test game over when player 2 wins in PvP"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 2, 'tokan_pisteet': 5, 'tasapelit': 1}
        
        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'Pelaaja 2 voitti pelin!' in response.data
    
    def test_game_over_ai_wins(self, client):
        """Test game over when AI wins"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'b'
            sess['tuomari'] = {'ekan_pisteet': 1, 'tokan_pisteet': 3, 'tasapelit': 0}
        
        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'Tietokone voitti pelin!' in response.data
    
    def test_game_over_advanced_ai_wins(self, client):
        """Test game over when advanced AI wins"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'c'
            sess['tuomari'] = {'ekan_pisteet': 2, 'tokan_pisteet': 3, 'tasapelit': 1}
        
        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'Tietokone voitti pelin!' in response.data


class TestAILogic:
    """Test AI move generation"""
    
    def test_simple_ai_cycles_through_moves(self, client):
        """Test that simple AI cycles k -> p -> s -> k"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'b'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_siirto'] = 0
        
        # First move should be 'p' (0+1 % 3 = 1)
        client.post('/move', data={'ekan_siirto': 'k'})
        
        with client.session_transaction() as sess:
            first_ai_state = sess['ai_siirto']
            assert first_ai_state == 1
        
        # Second move should be 's' (1+1 % 3 = 2)
        client.post('/move', data={'ekan_siirto': 'k'})
        
        with client.session_transaction() as sess:
            assert sess['ai_siirto'] == 2
        
        # Third move should be 'k' (2+1 % 3 = 0)
        client.post('/move', data={'ekan_siirto': 'k'})
        
        with client.session_transaction() as sess:
            assert sess['ai_siirto'] == 0
    
    def test_advanced_ai_memory_storage(self, client):
        """Test that advanced AI stores player moves in memory"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'c'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_muisti'] = [None] * 10
            sess['ai_vapaa_indeksi'] = 0
        
        # Make several moves
        moves = ['k', 'p', 's', 'k', 'p']
        for move in moves:
            client.post('/move', data={'ekan_siirto': move})
        
        with client.session_transaction() as sess:
            assert sess['ai_muisti'][:5] == moves
            assert sess['ai_vapaa_indeksi'] == 5
    
    def test_advanced_ai_memory_overflow(self, client):
        """Test that advanced AI shifts memory when full"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'c'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_muisti'] = ['k'] * 10
            sess['ai_vapaa_indeksi'] = 10
        
        # Make one more move
        client.post('/move', data={'ekan_siirto': 'p'})
        
        with client.session_transaction() as sess:
            # Memory should have shifted and new move added
            assert sess['ai_muisti'][9] == 'p'
            assert sess['ai_vapaa_indeksi'] == 10
    
    def test_advanced_ai_initial_moves(self, client):
        """Test advanced AI behavior on first moves"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'c'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
            sess['ai_muisti'] = [None] * 10
            sess['ai_vapaa_indeksi'] = 0
        
        # First move - AI should return 'k' when memory is empty
        response = client.post('/move', data={'ekan_siirto': 'k'}, follow_redirects=True)
        assert response.status_code == 200


class TestFullGameFlow:
    """Test complete game flows"""
    
    def test_complete_pvp_game_flow(self, client):
        """Test a complete player vs player game from start to finish"""
        # Start game
        client.post('/start', data={'game_type': 'a'})
        
        # Play 3 rounds where player 1 always wins
        for i in range(3):
            response = client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 's'})
        
        # Should redirect to game over
        with client.session_transaction() as sess:
            assert sess['game_over'] is True
            assert sess['tuomari']['ekan_pisteet'] == 3
        
        # Check game over page
        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'Pelaaja 1 voitti' in response.data
    
    def test_complete_ai_game_flow(self, client):
        """Test a complete game against simple AI"""
        # Start game
        client.post('/start', data={'game_type': 'b'})
        
        # Play enough rounds
        for i in range(10):
            with client.session_transaction() as sess:
                if sess.get('game_over'):
                    break
            client.post('/move', data={'ekan_siirto': 'k'})
        
        # Game should be over
        with client.session_transaction() as sess:
            total_wins = sess['tuomari']['ekan_pisteet'] + sess['tuomari']['tokan_pisteet']
            assert total_wins >= 5
    
    def test_mixed_results_game(self, client):
        """Test a game with mixed results (wins, losses, ties)"""
        with client.session_transaction() as sess:
            sess['game_type'] = 'a'
            sess['tuomari'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
            sess['round'] = 1
            sess['game_over'] = False
        
        # Tie
        client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 'k'})
        # Player 1 wins
        client.post('/move', data={'ekan_siirto': 'k', 'tokan_siirto': 's'})
        # Player 2 wins
        client.post('/move', data={'ekan_siirto': 's', 'tokan_siirto': 'k'})
        
        with client.session_transaction() as sess:
            assert sess['tuomari']['ekan_pisteet'] == 1
            assert sess['tuomari']['tokan_pisteet'] == 1
            assert sess['tuomari']['tasapelit'] == 1
