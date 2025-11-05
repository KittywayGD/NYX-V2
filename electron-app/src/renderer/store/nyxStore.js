/**
 * Zustand Store pour l'état global de NYX-V2
 */

import { create } from 'zustand';

const useNyxStore = create((set, get) => ({
  // Chat state
  messages: [],
  currentQuery: '',
  isProcessing: false,

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
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      ...message,
      id: Date.now() + Math.random(),
      timestamp: new Date().toISOString(),
    }]
  })),

  clearMessages: () => set({ messages: [] }),

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
      console.error('Error querying NYX:', error);
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
      console.error('Error initializing NYX:', error);
      set({ isConnected: false });
    }
  },
}));

export default useNyxStore;
