def set_global_style(app):
    app.setStyleSheet("""
        QWidget {
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            font-size: 14px;
            background-color: #ffffff;
            color: #333333;
        }
        
        QLabel {
            color: #2c3e50;
            background-color: transparent;
        }
        
        QWidget > QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 4px;
        }
        
        QWidget > QPushButton:hover {
            background-color: #45a049;
        }
        
        QWidget > #start-button, QWidget > #submit-button, QWidget > #record-button, QWidget > #restart-button {
            background-color: #2196F3;
            font-size: 18px;
            padding: 15px 30px;
        }
        
        QWidget > #start-button:hover, QWidget > #submit-button:hover, QWidget > #record-button:hover, QWidget > #restart-button:hover {
            background-color: #1976D2;
        }
        
        QLineEdit, QTextEdit {
            padding: 8px;
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            background-color: #f8f8f8;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border-color: #4CAF50;
            outline: none;
        }
        
        #welcome-title {
            font-size: 36px;
            color: #2c3e50;
            font-weight: bold;
        }
        
        #question-text {
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        #result-label {
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        
        #correct-answer {
            color: #4CAF50;
        }
        
        #incorrect-answer {
            color: #F44336;
        }
        
        #spectrum-frame {
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            background-color: #f8f8f8;
            padding: 10px;
        }

        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
