@echo off
title Upload Pages Optimisees - DOXA
color 0A

echo.
echo ================================================================
echo                   UPLOAD PAGES OPTIMISEES
echo                      DOXA Investments
echo ================================================================
echo.

echo [INFO] Preparation des fichiers optimises...

REM Creer le package avec les nouvelles pages
if not exist "package-pages-optimisees" mkdir "package-pages-optimisees"

echo [INFO] Copie des pages ameliorees...
copy "index-ameliore.html" "package-pages-optimisees\index.html"
copy "404.html" "package-pages-optimisees\"
copy "maintenance.html" "package-pages-optimisees\"

REM Copier le fichier htaccess pour les erreurs 404
echo [INFO] Creation du fichier .htaccess...
echo # Configuration Apache pour DOXA Investments > "package-pages-optimisees\.htaccess"
echo # Redirection erreur 404 >> "package-pages-optimisees\.htaccess"
echo ErrorDocument 404 /404.html >> "package-pages-optimisees\.htaccess"
echo. >> "package-pages-optimisees\.htaccess"
echo # Redirection maintenance si necessaire >> "package-pages-optimisees\.htaccess"
echo # RewriteEngine On >> "package-pages-optimisees\.htaccess"
echo # RewriteCond %%{REQUEST_URI} !^/maintenance.html$ >> "package-pages-optimisees\.htaccess"
echo # RewriteRule ^(.*)$ /maintenance.html [R=302,L] >> "package-pages-optimisees\.htaccess"

REM Copier les dossiers essentiels
echo [INFO] Copie du frontend...
if exist "frontend\build" (
    xcopy "frontend\build\*" "package-pages-optimisees\frontend\" /E /I /Y
) else (
    echo [WARNING] Dossier frontend\build non trouve
)

echo [INFO] Copie du backend...
if exist "backend\upload-final" (
    xcopy "backend\upload-final\*" "package-pages-optimisees\backend\" /E /I /Y
) else (
    echo [WARNING] Dossier backend\upload-final non trouve
)

echo.
echo ================================================================
echo                    PACKAGE PRET POUR UPLOAD
echo ================================================================
echo.
echo [SUCCESS] Package cree : package-pages-optimisees\
echo.
echo INSTRUCTIONS D'UPLOAD :
echo 1. Connectez-vous a FileZilla
echo 2. Naviguez vers le dossier htdocs de votre site
echo 3. Uploadez TOUT le contenu de package-pages-optimisees\
echo 4. Verifiez que index.html remplace l'ancien
echo.
echo PAGES AMELIOREES :
echo - Page d'accueil : Design moderne et responsif
echo - Page 404 : Redirection intelligente
echo - Page maintenance : Statut en temps reel
echo - Configuration Apache : Gestion d'erreurs
echo.
echo ================================================================
echo.

pause
explorer "package-pages-optimisees"
