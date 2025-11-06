/**
 * Zustand Store pour l'état global de NYX-V2
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Generate unique IDs for messages
let messageIdCounter = 0;
const generateMessageId = () => {
  return `msg_${Date.now()}_${++messageIdCounter}`;
};

// Constants
const MAX_MESSAGES = 1000; // Maximum messages to keep in memory
const MAX_VISIBLE_MESSAGES = 100; // Messages to show at once

const useNyxStore = create(
  persist(
    (set, get) => ({
      // Chat state
      messages: [],
      currentQuery: '',
      isProcessing: false,
      messageOffset: 0, // For pagination

  // Sandbox state
  activeSandbox: null, // 'math' | 'physics' | 'electronics' | null
  sandboxData: null,
  sandboxVisible: false,

  // System state
  nyxStatus: null,
  modules: [],
  isConnected: false,

  // Settings
  settings: {
    theme: 'dark',
    autoOpenSandbox: true,
    showIntent: true,
  },

  // Actions - Chat
  addMessage: (message) => set((state) => {
    const newMessage = {
      ...message,
      id: generateMessageId(),
      timestamp: new Date().toISOString(),
    };

    // Keep only last MAX_MESSAGES messages
    const updatedMessages = [...state.messages, newMessage];
    if (updatedMessages.length > MAX_MESSAGES) {
      return { messages: updatedMessages.slice(-MAX_MESSAGES) };
    }

    return { messages: updatedMessages };
  }),

  clearMessages: () => set({ messages: [], messageOffset: 0 }),

  // Pagination
  getVisibleMessages: () => {
    const { messages, messageOffset } = get();
    const start = Math.max(0, messages.length - MAX_VISIBLE_MESSAGES - messageOffset);
    const end = messages.length - messageOffset;
    return messages.slice(start, end);
  },

  loadMoreMessages: () => set((state) => ({
    messageOffset: Math.min(
      state.messageOffset + 50,
      Math.max(0, state.messages.length - MAX_VISIBLE_MESSAGES)
    ),
  })),

  resetMessageOffset: () => set({ messageOffset: 0 }),

  setCurrentQuery: (query) => set({ currentQuery: query }),

  setProcessing: (isProcessing) => set({ isProcessing }),

  // Actions - Sandbox
  setSandbox: (sandboxType, data) => set({
    activeSandbox: sandboxType,
    sandboxData: data,
    sandboxVisible: true,
  }),

  closeSandbox: () => set({
    sandboxVisible: false,
  }),

  clearSandbox: () => set({
    activeSandbox: null,
    sandboxData: null,
    sandboxVisible: false,
  }),

  // Actions - System
  setStatus: (status) => set({ nyxStatus: status, isConnected: true }),

  setModules: (modules) => set({ modules }),

  setConnectionStatus: (isConnected) => set({ isConnected }),

  // Actions - Settings
  updateSettings: (newSettings) => set((state) => ({
    settings: { ...state.settings, ...newSettings }
  })),

  // Actions - Query NYX
  queryNyx: async (query, context = null) => {
    const { addMessage, setProcessing, setSandbox, settings } = get();

    // Add user message
    addMessage({
      role: 'user',
      content: query,
    });

    setProcessing(true);

    try {
      // Detect intent first if enabled
      let intent = null;
      if (settings.showIntent) {
        const intentResult = await window.nyxAPI.detectIntent({ query, context });
        if (intentResult.success) {
          intent = intentResult.intent;
        }
      }

      // Query NYX
      const response = await window.nyxAPI.query({
        query,
        context,
        validate: true,
      });

      if (response.success) {
        // Add assistant message
        addMessage({
          role: 'assistant',
          content: response.result || response,
          intent,
        });

        // Open sandbox if needed
        if (intent?.requires_sandbox && settings.autoOpenSandbox) {
          // Determine sandbox type from domain
          const sandboxType = intent.domain;
          if (sandboxType && ['mathematics', 'physics', 'electronics'].includes(sandboxType)) {
            setSandbox(sandboxType, response);
          }
        }
      } else {
        addMessage({
          role: 'error',
          content: response.error || 'Une erreur est survenue',
        });
      }
    } catch (error) {
      // Log error via IPC instead of console
      if (window.nyxAPI?.error) {
        window.nyxAPI.error('Error querying NYX:', error);
      }
      addMessage({
        role: 'error',
        content: error.message || 'Erreur de connexion',
      });
    } finally {
      setProcessing(false);
    }
  },

  // Initialize
  initialize: async () => {
    try {
      // Get status
      const status = await window.nyxAPI.getStatus();
      if (status.success) {
        set({ nyxStatus: status, isConnected: true });
      }

      // Get modules
      const modulesResult = await window.nyxAPI.getModules();
      if (modulesResult.success) {
        set({ modules: modulesResult.modules });
      }

      // Add welcome message
      get().addMessage({
        role: 'assistant',
        content: {
          type: 'welcome',
          message: 'Bienvenue dans NYX-V2 ! Je suis votre assistant scientifique. Posez-moi des questions en mathématiques, physique ou électronique, et je peux également créer des visualisations interactives dans les bacs à sable.',
        },
      });

    } catch (error) {
      // Log error via IPC instead of console
      if (window.nyxAPI?.error) {
        window.nyxAPI.error('Error initializing NYX:', error);
      }
      set({ isConnected: false });
    }
  },
    }),
    {
      name: 'nyx-storage', // Persist key
      partialize: (state) => ({
        // Only persist settings and recent messages
        settings: state.settings,
        messages: state.messages.slice(-50), // Keep last 50 messages
      }),
    }
  )
);

export default useNyxStore;
