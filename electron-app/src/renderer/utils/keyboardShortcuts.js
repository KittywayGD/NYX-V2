/**
 * Keyboard Shortcuts System
 * Centralized keyboard shortcut management
 */

import { useEffect } from 'react';

/**
 * Available keyboard shortcuts
 */
export const SHORTCUTS = {
  SEND_MESSAGE: { key: 'Enter', ctrl: true, description: 'Envoyer le message' },
  CLEAR_CHAT: { key: 'l', ctrl: true, shift: true, description: 'Effacer le chat' },
  FOCUS_INPUT: { key: 'k', ctrl: true, description: 'Focus sur l\'input' },
  CLOSE_MODAL: { key: 'Escape', description: 'Fermer modal/sandbox' },
  EXPORT_CHAT: { key: 'e', ctrl: true, shift: true, description: 'Exporter le chat' },
  OPEN_SETTINGS: { key: ',', ctrl: true, description: 'Ouvrir les paramètres' },
};

/**
 * Format shortcut for display
 */
export function formatShortcut(shortcut) {
  const keys = [];
  if (shortcut.ctrl) keys.push('Ctrl');
  if (shortcut.shift) keys.push('Shift');
  if (shortcut.alt) keys.push('Alt');
  keys.push(shortcut.key);
  return keys.join(' + ');
}

/**
 * Check if event matches shortcut
 */
function matchesShortcut(event, shortcut) {
  const keyMatch = event.key.toLowerCase() === shortcut.key.toLowerCase();
  const ctrlMatch = shortcut.ctrl ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
  const shiftMatch = shortcut.shift ? event.shiftKey : !event.shiftKey;
  const altMatch = shortcut.alt ? event.altKey : !event.altKey;

  return keyMatch && ctrlMatch && shiftMatch && altMatch;
}

/**
 * Hook to register keyboard shortcuts
 * @param {Object} shortcuts - Map of shortcut names to handlers
 * @param {Array} deps - Dependencies array
 *
 * @example
 * useKeyboardShortcuts({
 *   SEND_MESSAGE: () => handleSend(),
 *   CLEAR_CHAT: () => handleClear(),
 * }, [handleSend, handleClear]);
 */
export function useKeyboardShortcuts(shortcuts, deps = []) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Don't trigger shortcuts when typing in an input (unless it's Enter)
      const isInputFocused =
        event.target.tagName === 'INPUT' ||
        event.target.tagName === 'TEXTAREA' ||
        event.target.isContentEditable;

      for (const [name, handler] of Object.entries(shortcuts)) {
        const shortcut = SHORTCUTS[name];
        if (!shortcut) continue;

        // Allow Enter in inputs for SEND_MESSAGE
        if (isInputFocused && shortcut.key !== 'Enter') {
          continue;
        }

        if (matchesShortcut(event, shortcut)) {
          event.preventDefault();
          event.stopPropagation();
          handler();
          break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, deps);
}

/**
 * Hook for global keyboard shortcuts
 */
export function useGlobalShortcuts(handlers) {
  useKeyboardShortcuts(handlers, [handlers]);
}
