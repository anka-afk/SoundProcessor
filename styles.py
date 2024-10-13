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
        }
        
        QWidget > #start-button:hover, QWidget > #submit-button:hover, QWidget > #record-button:hover, QWidget > #restart-button:hover {
            background-color: #1976D2;
        }

        QLineEdit, QTextEdit, QTextBrowser {
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 8px;
            background-color: #f8f8f8;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border-color: #4CAF50;
        }
        
        #welcome-title, #form-title, #question-title, #summary-title {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
            background-color: transparent;
        }
        
        #question-number {
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 15px;
            background-color: transparent;
        }
        
        #question-content, #question-hint {
            font-size: 16px;
            margin-bottom: 15px;
            line-height: 1.5;
            background-color: transparent;
            border: none;
            color: #333333;
        }
        
        #debug-output {
            font-family: 'Courier New', monospace;
            font-size: 12px;
            background-color: #f1f1f1;
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 10px;
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
