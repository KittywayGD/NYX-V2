/**
 * Settings Panel Component
 * User preferences and application configuration
 */

import React, { memo, useState } from 'react';
import { X, Save, RotateCcw, Settings as SettingsIcon } from 'lucide-react';
import useNyxStore from '../store/nyxStore';

const SettingsPanel = memo(({ onClose }) => {
  const { settings, updateSettings } = useNyxStore();
  const [localSettings, setLocalSettings] = useState(settings);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    updateSettings(localSettings);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleReset = () => {
    const defaultSettings = {
      theme: 'dark',
      autoOpenSandbox: true,
      showIntent: true,
    };
    setLocalSettings(defaultSettings);
  };

  const handleChange = (key, value) => {
    setLocalSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="glass max-w-2xl w-full mx-4 rounded-lg border border-gray-700">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <SettingsIcon className="w-6 h-6 text-nyx-accent" />
            <h2 className="text-2xl font-bold">Paramètres</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
            aria-label="Fermer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Appearance Section */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Apparence</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <label className="font-medium">Thème</label>
                  <p className="text-sm text-gray-400">
                    Choisir l'apparence de l'interface
                  </p>
                </div>
                <select
                  value={localSettings.theme}
                  onChange={(e) => handleChange('theme', e.target.value)}
                  className="bg-nyx-dark border border-gray-600 rounded px-4 py-2 focus:outline-none focus:border-nyx-accent"
                >
                  <option value="dark">Sombre</option>
                  <option value="light">Clair</option>
                  <option value="auto">Automatique</option>
                </select>
              </div>
            </div>
          </div>

          {/* Behavior Section */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Comportement</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <label className="font-medium">Ouvrir sandbox automatiquement</label>
                  <p className="text-sm text-gray-400">
                    Ouvre le sandbox quand applicable
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={localSettings.autoOpenSandbox}
                    onChange={(e) => handleChange('autoOpenSandbox', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-nyx-accent rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-nyx-accent"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="font-medium">Afficher l'intention détectée</label>
                  <p className="text-sm text-gray-400">
                    Affiche l'intention détectée pour chaque requête
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={localSettings.showIntent}
                    onChange={(e) => handleChange('showIntent', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-nyx-accent rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-nyx-accent"></div>
                </label>
              </div>
            </div>
          </div>

          {/* About Section */}
          <div>
            <h3 className="text-lg font-semibold mb-3">À propos</h3>
            <div className="bg-nyx-dark/50 p-4 rounded-lg border border-gray-700">
              <p className="text-sm text-gray-400">
                <strong>NYX-V2</strong> - Assistant Scientifique Intelligent
              </p>
              <p className="text-xs text-gray-500 mt-2">
                Version 2.0.0 • Built with React + FastAPI
              </p>
              <div className="mt-3 pt-3 border-t border-gray-700">
                <p className="text-xs text-gray-500">
                  © 2024 NYX-V2 Team. Tous droits réservés.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-700">
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 hover:bg-gray-700 rounded transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Réinitialiser
          </button>

          <div className="flex gap-3">
            {saved && (
              <span className="px-4 py-2 text-green-400 text-sm">
                ✓ Sauvegardé
              </span>
            )}
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-6 py-2 bg-nyx-accent hover:bg-nyx-accent-hover rounded transition-colors"
            >
              <Save className="w-4 h-4" />
              Sauvegarder
            </button>
          </div>
        </div>
      </div>
    </div>
  );
});

SettingsPanel.displayName = 'SettingsPanel';

export default SettingsPanel;
