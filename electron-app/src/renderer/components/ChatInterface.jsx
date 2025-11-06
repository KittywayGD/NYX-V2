import { useState, useRef, useEffect } from 'react';
import useNyxStore from '../store/nyxStore';
import { Send, Loader2, Download, Trash2, Zap } from 'lucide-react';
import { useKeyboardShortcuts } from '../utils/keyboardShortcuts';

function ChatInterface() {
  const { messages, queryNyx, isProcessing, currentQuery, setCurrentQuery, clearMessages } = useNyxStore();
  const [input, setInput] = useState('');
  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (input.trim() && !isProcessing) {
      queryNyx(input);
      setInput('');
    }
  };

  const handleClearChat = () => {
    if (confirm('Êtes-vous sûr de vouloir effacer tout l\'historique ?')) {
      clearMessages();
    }
  };

  const handleExportChat = (format = 'json') => {
    const timestamp = new Date().toISOString().split('T')[0];
    let content, mimeType, extension;

    if (format === 'json') {
      content = JSON.stringify(messages, null, 2);
      mimeType = 'application/json';
      extension = 'json';
    } else if (format === 'markdown') {
      content = messages
        .map((msg) => {
          const role = msg.role === 'user' ? '**Vous**' : '**NYX**';
          const text = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content, null, 2);
          return `${role}: ${text}\n`;
        })
        .join('\n');
      mimeType = 'text/markdown';
      extension = 'md';
    } else if (format === 'text') {
      content = messages
        .map((msg) => {
          const role = msg.role === 'user' ? 'Vous' : 'NYX';
          const text = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
          return `${role}: ${text}`;
        })
        .join('\n\n');
      mimeType = 'text/plain';
      extension = 'txt';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nyx-chat-${timestamp}.${extension}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Keyboard shortcuts
  useKeyboardShortcuts(
    {
      SEND_MESSAGE: handleSubmit,
      CLEAR_CHAT: handleClearChat,
      FOCUS_INPUT: () => inputRef.current?.focus(),
      EXPORT_CHAT: () => handleExportChat('json'),
    },
    [input, isProcessing, messages]
  );

  return (
    <div className="flex flex-col h-full">
      {/* Header - Cyberpunk Style */}
      <div className="cyber-glass px-6 py-4 border-b border-cyber-cyan border-opacity-30 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-display font-bold text-glow-cyan holographic">NYX-V2</h2>
          <p className="text-sm text-cyber-cyan uppercase tracking-wider font-display">Math • Physique • Électronique</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleExportChat('json')}
            className="p-2 hover:bg-cyber-cyan hover:bg-opacity-10 rounded transition-all duration-300 text-cyber-cyan hover:shadow-neon-cyan group"
            title="Exporter le chat (Ctrl+Shift+E)"
            aria-label="Export chat"
          >
            <Download className="w-5 h-5 group-hover:animate-bounce" />
          </button>
          <button
            onClick={handleClearChat}
            className="p-2 hover:bg-cyber-error hover:bg-opacity-10 rounded transition-all duration-300 text-cyber-error hover:shadow-neon-pink group"
            title="Effacer le chat (Ctrl+Shift+L)"
            aria-label="Clear chat"
          >
            <Trash2 className="w-5 h-5 group-hover:animate-bounce" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isProcessing && (
          <div className="flex items-center gap-3 text-cyber-cyan">
            <Loader2 className="w-5 h-5 animate-spin" style={{ filter: 'drop-shadow(0 0 8px rgba(6, 182, 212, 0.8))' }} />
            <span className="font-display uppercase text-sm tracking-wider animate-pulse">NYX calcule...</span>
            <Zap className="w-4 h-4 animate-pulse" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input - Cyberpunk Style */}
      <div className="cyber-glass p-4 border-t border-cyber-cyan border-opacity-30">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="▸ ENTREZ VOTRE REQUÊTE SCIENTIFIQUE..."
            className="flex-1 bg-cyber-navy bg-opacity-50 border border-cyber-cyan border-opacity-30 rounded-lg px-4 py-3 focus:outline-none focus:border-cyber-cyan focus:shadow-neon-cyan transition-all duration-300 font-display text-cyber-cyan placeholder-cyber-cyan placeholder-opacity-40"
            disabled={isProcessing}
            aria-label="Question scientifique"
          />
          <button
            type="submit"
            disabled={isProcessing || !input.trim()}
            className="cyber-button disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg transition-all duration-300 flex items-center gap-2 font-display"
          >
            {isProcessing ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span className="hidden sm:inline font-semibold">ENVOYER</span>
          </button>
        </form>

        {/* Quick Examples - Cyberpunk Style */}
        <div className="mt-3 flex flex-wrap gap-2">
          <QuickButton onClick={() => setInput('Tracer x² - 4')}>
            <span className="text-cyber-purple mr-1">⚡</span> Tracer x² - 4
          </QuickButton>
          <QuickButton onClick={() => setInput('Simuler un pendule')}>
            <span className="text-cyber-cyan mr-1">⚙</span> Simuler un pendule
          </QuickButton>
          <QuickButton onClick={() => setInput('Circuit RC')}>
            <span className="text-cyber-pink mr-1">⚡</span> Circuit RC
          </QuickButton>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';

  return (
    <div className={`fade-in ${isUser ? 'flex justify-end' : ''}`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser
            ? 'cyber-glass-pink text-white border-cyber-magenta border-opacity-50'
            : isError
            ? 'cyber-glass bg-cyber-error bg-opacity-10 border border-cyber-error'
            : 'cyber-glass'
        }`}
      >
        {/* Intent badge - Cyberpunk Style */}
        {message.intent && !isUser && (
          <div className="mb-3 flex gap-2 text-xs">
            <span className="px-3 py-1 bg-cyber-navy bg-opacity-50 border border-cyber-cyan border-opacity-30 rounded font-display text-cyber-cyan uppercase tracking-wide">
              {message.intent.domain}
            </span>
            <span className="px-3 py-1 bg-cyber-navy bg-opacity-50 border border-cyber-purple border-opacity-30 rounded font-display text-cyber-purple uppercase tracking-wide">
              {message.intent.action}
            </span>
            <span className="px-3 py-1 bg-cyber-navy bg-opacity-50 border border-cyber-success border-opacity-30 rounded font-display text-cyber-success uppercase tracking-wide">
              {Math.round(message.intent.confidence * 100)}%
            </span>
          </div>
        )}

        {/* Content */}
        {typeof message.content === 'string' ? (
          <p className="whitespace-pre-wrap text-gray-100 leading-relaxed">{message.content}</p>
        ) : message.content.type === 'welcome' ? (
          <div>
            <p className="font-display font-semibold mb-3 text-lg text-glow-cyan">
              <span className="text-2xl mr-2">👋</span>
              {message.content.message}
            </p>
            <p className="text-sm text-cyber-cyan mt-3 mb-2 uppercase tracking-wide font-display">
              ▸ Exemples de commandes:
            </p>
            <ul className="text-sm text-gray-300 mt-2 space-y-2">
              <li className="flex items-start">
                <span className="text-cyber-purple mr-2">▸</span>
                "Tracer la fonction sin(x)*exp(-x)"
              </li>
              <li className="flex items-start">
                <span className="text-cyber-cyan mr-2">▸</span>
                "Simuler un projectile lancé à 45°"
              </li>
              <li className="flex items-start">
                <span className="text-cyber-pink mr-2">▸</span>
                "Analyser un circuit RC avec R=1kΩ, C=1µF"
              </li>
            </ul>
          </div>
        ) : (
          <pre className="text-sm overflow-x-auto code-block">
            {JSON.stringify(message.content, null, 2)}
          </pre>
        )}

        {/* Timestamp */}
        <div className="text-xs text-cyber-cyan text-opacity-50 mt-3 font-display uppercase tracking-wider">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

function QuickButton({ onClick, children }) {
  return (
    <button
      onClick={onClick}
      className="text-sm px-4 py-2 bg-cyber-navy bg-opacity-30 border border-cyber-cyan border-opacity-30 rounded hover:border-cyber-cyan hover:bg-cyber-cyan hover:bg-opacity-10 hover:shadow-neon-cyan transition-all duration-300 font-display uppercase tracking-wide text-cyber-cyan"
    >
      {children}
    </button>
  );
}

export default ChatInterface;
