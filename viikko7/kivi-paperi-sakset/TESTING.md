# Testing Guide

## Running Tests

### Using Poetry (Recommended)

```bash
# Run all tests
poetry run pytest tests/ -v

# Run with coverage report
poetry run pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_app.py -v

# Run specific test class
poetry run pytest tests/test_game_logic.py::TestTuomari -v

# Run specific test
poetry run pytest tests/test_app.py::TestRoutes::test_index_route -v
```

### Using the test script

```bash
./run_tests.sh
```

### Direct Python

```bash
.venv/bin/python -m pytest tests/ -v
```

## Test Structure

The test suite is organized into two main files:

### test_app.py
Tests for the Flask web application:
- **TestRoutes**: Basic route functionality (index, redirects)
- **TestStartGame**: Game initialization for all game types
- **TestPlayRoute**: Play page rendering and state management
- **TestMakeMove**: Move processing, scoring, and game logic
- **TestGameOver**: Game completion and winner display
- **TestAILogic**: AI move generation and memory management
- **TestFullGameFlow**: Complete game scenarios from start to finish

### test_game_logic.py  
Tests for the core game logic classes:
- **TestTuomari**: Referee class (score tracking, win detection)
- **TestTekoaly**: Simple AI behavior
- **TestTekoalyParannettu**: Advanced AI with pattern learning
- **TestLuoPeli**: Game factory
- **TestKiviPaperiSakset**: Base game class
- **TestKPSPelaajaVsPelaaja**: Player vs Player mode
- **TestKPSTekoaly**: Player vs Simple AI mode
- **TestKPSParempiTekoaly**: Player vs Advanced AI mode

## Test Coverage

The test suite covers:

✅ All Flask routes and HTTP methods
✅ Session management
✅ Game initialization for all three game types
✅ Move validation
✅ Score calculation (wins, losses, ties)
✅ 5-win game ending feature
✅ Simple AI cycling behavior
✅ Advanced AI pattern learning and memory management
✅ Edge cases (invalid inputs, missing session data)
✅ Complete game flows from start to finish
✅ All core game logic classes
✅ AI implementations

## Test Count

- **Route tests**: 11 tests
- **Start game tests**: 6 tests  
- **Play route tests**: 5 tests
- **Move tests**: 14 tests
- **Game over tests**: 4 tests
- **AI logic tests**: 5 tests
- **Full game flow tests**: 3 tests
- **Game logic tests**: 38 tests

**Total: 86 comprehensive tests**

## Expected Results

All tests should pass with 100% success rate. The suite tests:

1. **Web UI functionality** - All routes, forms, and redirects
2. **Game rules** - Rock beats scissors, scissors beats paper, paper beats rock
3. **Score tracking** - Accurate win/loss/tie counting
4. **5-win limit** - Games automatically end when either player reaches 5 wins
5. **AI behavior** - Both simple and advanced AI work correctly
6. **Session management** - Game state persists across requests
7. **Error handling** - Invalid inputs handled gracefully

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: poetry install --with dev
      - name: Run tests
        run: poetry run pytest tests/ -v --cov=src
```

## Writing New Tests

When adding new features:

1. Add tests to the appropriate test file
2. Use descriptive test names: `test_<what>_<condition>_<expected>`
3. Follow the AAA pattern: Arrange, Act, Assert
4. Use fixtures from `conftest.py` for Flask app and client
5. Test both success and failure cases
6. Verify session state changes for stateful operations

Example:

```python
def test_new_feature_with_valid_input(self, client):
    """Test description"""
    # Arrange
    with client.session_transaction() as sess:
        sess['game_type'] = 'a'
    
    # Act  
    response = client.post('/new-endpoint', data={'key': 'value'})
    
    # Assert
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['expected_key'] == 'expected_value'
```
