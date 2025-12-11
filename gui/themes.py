THEMES = {
    'light': """
    QWidget {
        background-color: #f0f0f0;
        color: #000000;
    }
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
    }
    """,
    'dark': """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #3c3c3c;
        border: 1px solid #555555;
    }
    QPushButton:hover {
        background-color: #4c4c4c;
    }
    """,
    'neon': """
    QWidget {
        background-color: #000000;
        color: #00ff00;
    }
    QPushButton {
        background-color: #001100;
        border: 1px solid #00ff00;
    }
    QPushButton:hover {
        background-color: #002200;
    }
    """
}

def get_theme_css(theme):
    return THEMES.get(theme, THEMES['light'])