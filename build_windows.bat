@echo off
echo === Compilation de l'application Logistique pour WINDOWS ===
:: Vérification de la présence de Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH !
    echo Veuillez installer Python depuis python.org et cocher "Add Python to PATH".
    pause
    exit /b
)

:: Création de l'environnement virtuel pour éviter de polluer le système
IF NOT EXIST venv (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

:: Activation et installation
call venv\Scripts\activate.bat
echo Installation des dependances...
pip install pulp matplotlib pyinstaller

echo Creation de l'executable Windows (.exe)...
pyinstaller --noconsole --onefile --collect-all pulp --name "Logistique_Optimisation_Windows" main_gui.py

echo.
echo === Termine ! L'executable Windows (.exe) se trouve dans le dossier 'dist' ===
pause
