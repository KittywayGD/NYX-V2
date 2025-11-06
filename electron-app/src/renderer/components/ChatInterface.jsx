import { useState, useRef, useEffect } from 'react';
import useNyxStore from '../store/nyxStore';
import { Send, Loader2, Download, Trash2 } from 'lucide-react';
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
      {/* Header */}
      <div className="glass px-6 py-4 border-b border-gray-700 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-nyx-accent">NYX-V2 Assistant</h2>
          <p className="text-sm text-gray-400">Mathématiques • Physique • Électronique</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleExportChat('json')}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
            title="Exporter le chat (Ctrl+Shift+E)"
            aria-label="Export chat"
          >
            <Download className="w-5 h-5" />
          </button>
          <button
            onClick={handleClearChat}
            className="p-2 hover:bg-gray-700 rounded transition-colors text-red-400"
            title="Effacer le chat (Ctrl+Shift+L)"
            aria-label="Clear chat"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isProcessing && (
          <div className="flex items-center gap-2 text-gray-400">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>NYX réfléchit...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="glass p-4 border-t border-gray-700">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question scientifique... (Ctrl+Enter pour envoyer)"
            className="flex-1 bg-nyx-dark border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-nyx-accent transition-colors"
            disabled={isProcessing}
            aria-label="Question scientifique"
          />
          <button
            type="submit"
            disabled={isProcessing || !input.trim()}
            className="bg-nyx-accent hover:bg-nyx-accent-hover disabled:bg-gray-600 disabled:cursor-not-allowed px-6 py-2 rounded-lg transition-colors flex items-center gap-2"
          >
            {isProcessing ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span className="hidden sm:inline">Envoyer</span>
          </button>
        </form>

        {/* Quick Examples */}
        <div className="mt-3 flex flex-wrap gap-2">
          <QuickButton onClick={() => setInput('Tracer x² - 4')}>
            Tracer x² - 4
          </QuickButton>
          <QuickButton onClick={() => setInput('Simuler un pendule')}>
            Simuler un pendule
          </QuickButton>
          <QuickButton onClick={() => setInput('Circuit RC')}>
            Circuit RC
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
            ? 'bg-nyx-accent text-white'
            : isError
            ? 'bg-nyx-error bg-opacity-20 border border-nyx-error'
            : 'glass'
        }`}
      >
        {/* Intent badge */}
        {message.intent && !isUser && (
          <div className="mb-2 flex gap-2 text-xs">
            <span className="px-2 py-1 bg-nyx-dark rounded">
              {message.intent.domain}
            </span>
            <span className="px-2 py-1 bg-nyx-dark rounded">
              {message.intent.action}
            </span>
            <span className="px-2 py-1 bg-nyx-dark rounded">
              {Math.round(message.intent.confidence * 100)}%
            </span>
          </div>
        )}

        {/* Content */}
        {typeof message.content === 'string' ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : message.content.type === 'welcome' ? (
          <div>
            <p className="font-semibold mb-2">👋 {message.content.message}</p>
            <p className="text-sm text-gray-400 mt-2">
              Exemples de commandes:
            </p>
            <ul className="text-sm text-gray-400 mt-1 space-y-1">
              <li>• "Tracer la fonction sin(x)*exp(-x)"</li>
              <li>• "Simuler un projectile lancé à 45°"</li>
              <li>• "Analyser un circuit RC avec R=1kΩ, C=1µF"</li>
            </ul>
          </div>
        ) : (
          <pre className="text-sm overflow-x-auto">
            {JSON.stringify(message.content, null, 2)}
          </pre>
        )}

        {/* Timestamp */}
        <div className="text-xs text-gray-500 mt-2">
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
      className="text-sm px-3 py-1 bg-nyx-dark border border-gray-600 rounded hover:border-nyx-accent transition-colors"
    >
      {children}
    </button>
  );
}

export default ChatInterface;
