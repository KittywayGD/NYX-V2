/**
 * Electron Main Process
 * Gère la fenêtre principale et la communication avec l'API
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

// Configuration
const API_URL = process.env.API_URL || 'http://localhost:8000';
const isDev = process.env.NODE_ENV !== 'production';

let mainWindow = null;

// Créer la fenêtre principale
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, '../preload/preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#1e293b',
      symbolColor: '#ffffff',
      height: 40,
    },
    backgroundColor: '#0f172a',
    show: false,
  });

  // Charger l'application
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../../dist-renderer/index.html'));
  }

  // Afficher quand prêt
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Nettoyer
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Démarrage de l'application
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quitter sur fermeture de toutes les fenêtres (sauf macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// ============================================================================
// IPC Handlers - Communication avec le renderer
// ============================================================================

// Query NYX
ipcMain.handle('nyx:query', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/query`, data);
    return response.data;
  } catch (error) {
    console.error('Error querying NYX:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Detect Intent
ipcMain.handle('nyx:intent', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/intent/detect`, data);
    return response.data;
  } catch (error) {
    console.error('Error detecting intent:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Get Status
ipcMain.handle('nyx:status', async () => {
  try {
    const response = await axios.get(`${API_URL}/api/status`);
    return response.data;
  } catch (error) {
    console.error('Error getting status:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Get Modules
ipcMain.handle('nyx:modules', async () => {
  try {
    const response = await axios.get(`${API_URL}/api/modules`);
    return response.data;
  } catch (error) {
    console.error('Error getting modules:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Math Sandbox - Plot
ipcMain.handle('sandbox:math:plot', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/sandbox/math/plot`, data);
    return response.data;
  } catch (error) {
    console.error('Error plotting:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Math Sandbox - Animate
ipcMain.handle('sandbox:math:animate', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/sandbox/math/animate`, data);
    return response.data;
  } catch (error) {
    console.error('Error animating:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Physics Sandbox - Simulate
ipcMain.handle('sandbox:physics:simulate', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/sandbox/physics/simulate`, data);
    return response.data;
  } catch (error) {
    console.error('Error simulating physics:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Electronics Sandbox - Simulate
ipcMain.handle('sandbox:electronics:simulate', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/sandbox/electronics/simulate`, data);
    return response.data;
  } catch (error) {
    console.error('Error simulating circuit:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Sandbox Général - Execute
ipcMain.handle('sandbox:execute', async (event, data) => {
  try {
    const response = await axios.post(`${API_URL}/api/sandbox/execute`, data);
    return response.data;
  } catch (error) {
    console.error('Error executing sandbox:', error);
    return {
      success: false,
      error: error.message,
    };
  }
});

// Health Check
ipcMain.handle('api:health', async () => {
  try {
    const response = await axios.get(`${API_URL}/health`);
    return response.data;
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
    };
  }
});

// Log to console (pour debug)
ipcMain.on('log', (event, ...args) => {
  console.log('[Renderer]:', ...args);
});

// Error logging
ipcMain.on('error', (event, ...args) => {
  console.error('[Renderer Error]:', ...args);
});
