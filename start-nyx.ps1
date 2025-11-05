###########################################
# NYX-V2 Startup Script (Windows)
# Lance tout le système d'une seule commande
###########################################

# Banner
Write-Host ""
Write-Host "╔═══════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║          NYX-V2 Startup               ║" -ForegroundColor Blue
Write-Host "║  Assistant Scientifique Intelligent   ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Variables globales pour les process
$apiProcess = $null
$electronProcess = $null

# Fonction de nettoyage
function Cleanup {
    Write-Host "`n🛑 Arrêt de NYX-V2..." -ForegroundColor Yellow

    if ($apiProcess) {
        Write-Host "   Arrêt de l'API..." -ForegroundColor Yellow
        Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
    }

    if ($electronProcess) {
        Write-Host "   Arrêt d'Electron..." -ForegroundColor Yellow
        Stop-Process -Id $electronProcess.Id -Force -ErrorAction SilentlyContinue
    }

    Write-Host "✓ NYX-V2 arrêté proprement" -ForegroundColor Green
    exit 0
}

# Trap Ctrl+C
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

# Étape 1: Vérifications
Write-Host "🔍 Vérification des prérequis..." -ForegroundColor Blue

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python 3 n'est pas installé!" -ForegroundColor Red
    exit 1
}

# Vérifier Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js n'est pas installé!" -ForegroundColor Red
    exit 1
}

# Vérifier Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "✓ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git n'est pas installé!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Étape 2: Git pull
Write-Host "📥 Mise à jour depuis GitHub..." -ForegroundColor Blue

if (Test-Path ".git") {
    $currentBranch = git branch --show-current
    Write-Host "   Branche actuelle: $currentBranch" -ForegroundColor Yellow

    # Stash local changes if any
    $gitStatus = git status -s
    if ($gitStatus) {
        Write-Host "   Sauvegarde des modifications locales..." -ForegroundColor Yellow
        git stash push -m "Auto-stash before pull at $(Get-Date)"
    }

    # Pull from main
    Write-Host "   git pull origin main" -ForegroundColor Yellow
    git pull origin main --no-edit

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Mise à jour réussie" -ForegroundColor Green
    } else {
        Write-Host "⚠ Mise à jour échouée (peut-être pas de connexion?)" -ForegroundColor Yellow
    }

    # Return to original branch if different
    if ($currentBranch -ne "main") {
        git checkout $currentBranch 2>$null
    }
} else {
    Write-Host "⚠ Pas un repository git, skip pull" -ForegroundColor Yellow
}

Write-Host ""

# Étape 3: Installer/Mettre à jour les dépendances Python
Write-Host "📦 Vérification des dépendances Python..." -ForegroundColor Blue

# Activate venv if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "   Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".venv\Scripts\Activate.ps1"
}

# Install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "   Installation des dépendances..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    pip install -q -r api\requirements.txt
    Write-Host "✓ Dépendances Python à jour" -ForegroundColor Green
}

Write-Host ""

# Étape 4: Installer/Mettre à jour les dépendances Node.js
Write-Host "📦 Vérification des dépendances Node.js..." -ForegroundColor Blue

Set-Location electron-app

if (!(Test-Path "node_modules")) {
    Write-Host "   Installation des dépendances Node.js (première fois)..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "   Mise à jour des dépendances..." -ForegroundColor Yellow
    npm install --silent
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dépendances Node.js à jour" -ForegroundColor Green
} else {
    Write-Host "✗ Erreur lors de l'installation des dépendances Node.js" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

Write-Host ""

# Étape 5: Lancer l'API Python
Write-Host "🚀 Lancement de l'API Backend..." -ForegroundColor Blue

# Créer le dossier logs s'il n'existe pas
New-Item -ItemType Directory -Force -Path logs | Out-Null

Set-Location api
$apiProcess = Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow -PassThru -RedirectStandardOutput "..\logs\api.log" -RedirectStandardError "..\logs\api-error.log"
Set-Location ..

Write-Host "✓ API démarrée (PID: $($apiProcess.Id))" -ForegroundColor Green
Write-Host "   URL: http://localhost:8000" -ForegroundColor Yellow
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

# Attendre que l'API soit prête
Write-Host "⏳ Attente du démarrage de l'API..." -ForegroundColor Blue
$apiReady = $false
for ($i = 1; $i -le 30; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ API prête!" -ForegroundColor Green
            $apiReady = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline
    }
}

if (!$apiReady) {
    Write-Host "`n⚠ L'API met du temps à démarrer, mais on continue..." -ForegroundColor Yellow
}

Write-Host ""

# Étape 6: Lancer l'application Electron
Write-Host "🚀 Lancement de l'application Electron..." -ForegroundColor Blue

Set-Location electron-app
$electronProcess = Start-Process -FilePath "npm" -ArgumentList "start" -NoNewWindow -PassThru
Set-Location ..

Write-Host "✓ Electron démarré (PID: $($electronProcess.Id))" -ForegroundColor Green
Write-Host ""

# Étape 7: Monitoring
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              NYX-V2 EST MAINTENANT ACTIF!              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Informations:" -ForegroundColor Blue
Write-Host "   API PID: $($apiProcess.Id)"
Write-Host "   Electron PID: $($electronProcess.Id)"
Write-Host "   API URL: http://localhost:8000"
Write-Host "   Logs: .\logs\"
Write-Host ""
Write-Host "💡 Appuyez sur Ctrl+C pour arrêter NYX-V2" -ForegroundColor Yellow
Write-Host ""

# Afficher les logs en temps réel
Write-Host "📋 Logs de l'API:" -ForegroundColor Blue
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Yellow

# Tail logs (PowerShell équivalent)
Get-Content -Path "logs\api.log" -Wait -Tail 20

# Attendre
Wait-Process -Id $apiProcess.Id

# Cleanup sera appelé automatiquement
Cleanup
