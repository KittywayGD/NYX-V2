/**
 * Electron Preload Script
 * Expose l'API NYX de manière sécurisée au renderer process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Exposer l'API NYX
contextBridge.exposeInMainWorld('nyxAPI', {
  // Queries
  query: (data) => ipcRenderer.invoke('nyx:query', data),
  detectIntent: (data) => ipcRenderer.invoke('nyx:intent', data),
  getStatus: () => ipcRenderer.invoke('nyx:status'),
  getModules: () => ipcRenderer.invoke('nyx:modules'),

  // Math Sandbox
  mathPlot: (data) => ipcRenderer.invoke('sandbox:math:plot', data),
  mathAnimate: (data) => ipcRenderer.invoke('sandbox:math:animate', data),

  // Physics Sandbox
  physicsSimulate: (data) => ipcRenderer.invoke('sandbox:physics:simulate', data),

  // Electronics Sandbox
  electronicsSimulate: (data) => ipcRenderer.invoke('sandbox:electronics:simulate', data),

  // Sandbox Général
  sandboxExecute: (data) => ipcRenderer.invoke('sandbox:execute', data),

  // Health
  healthCheck: () => ipcRenderer.invoke('api:health'),

  // Logging
  log: (...args) => ipcRenderer.send('log', ...args),
  error: (...args) => ipcRenderer.send('error', ...args),
});

// Exposer les infos système
contextBridge.exposeInMainWorld('systemInfo', {
  platform: process.platform,
  arch: process.arch,
  version: process.version,
});

// Console passthrough pour debug
contextBridge.exposeInMainWorld('console', {
  log: (...args) => console.log(...args),
  error: (...args) => console.error(...args),
  warn: (...args) => console.warn(...args),
  info: (...args) => console.info(...args),
});
