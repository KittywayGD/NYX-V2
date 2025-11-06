import { useEffect, useState, lazy, Suspense } from 'react';
import useNyxStore from './store/nyxStore';
import ErrorBoundary from './components/ErrorBoundary';
import { Activity } from 'lucide-react';

// Lazy load heavy components
const ChatInterface = lazy(() => import('./components/ChatInterface'));
const SandboxPanel = lazy(() => import('./components/SandboxPanel'));
const Sidebar = lazy(() => import('./components/Sidebar'));
const StatusBar = lazy(() => import('./components/StatusBar'));

// Loading fallback component - Cyberpunk style
const LoadingFallback = ({ message = 'Chargement...' }) => (
  <div className="flex items-center justify-center h-full">
    <div className="text-center">
      <Activity className="w-8 h-8 text-cyber-cyan animate-spin mx-auto mb-2" style={{ filter: 'drop-shadow(0 0 8px rgba(6, 182, 212, 0.8))' }} />
      <p className="text-cyber-cyan text-sm font-display uppercase tracking-wider">{message}</p>
    </div>
  </div>
);

function App() {
  const { initialize, isConnected, sandboxVisible } = useNyxStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      await initialize();
      setIsLoading(false);
    };
    init();
  }, [initialize]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-cyber-darker cyber-bg flex items-center justify-center scan-effect">
        <div className="text-center space-y-6">
          <div className="relative">
            <Activity className="w-16 h-16 text-cyber-cyan animate-spin mx-auto" style={{ filter: 'drop-shadow(0 0 12px rgba(6, 182, 212, 0.8))' }} />
            <div className="absolute inset-0 bg-cyber-cyan rounded-full blur-xl opacity-20 animate-pulse"></div>
          </div>
          <div>
            <h1 className="text-4xl font-display font-bold holographic mb-2">NYX-V2</h1>
            <p className="text-cyber-cyan text-sm uppercase tracking-widest animate-pulse">INITIALISATION DU SYSTÈME...</p>
          </div>
          <div className="flex gap-2 justify-center">
            <div className="w-2 h-2 bg-cyber-cyan rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
            <div className="w-2 h-2 bg-cyber-cyan rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-cyber-cyan rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="flex h-screen bg-cyber-darker cyber-bg text-white overflow-hidden scan-effect">
        {/* Sidebar */}
        <Suspense fallback={<LoadingFallback message="Chargement sidebar..." />}>
          <Sidebar />
        </Suspense>

        {/* Main content */}
        <div className="flex-1 flex flex-col">
          {/* Chat Interface */}
          <div className={`flex-1 ${sandboxVisible ? 'w-1/2' : 'w-full'}`}>
            <Suspense fallback={<LoadingFallback message="Chargement chat..." />}>
              <ChatInterface />
            </Suspense>
          </div>

          {/* Status Bar */}
          <Suspense fallback={<LoadingFallback message="Chargement status..." />}>
            <StatusBar />
          </Suspense>
        </div>

        {/* Sandbox Panel */}
        {sandboxVisible && (
          <div className="w-1/2 border-l border-cyber-cyan border-opacity-30 slide-in-right">
            <Suspense fallback={<LoadingFallback message="Chargement sandbox..." />}>
              <SandboxPanel />
            </Suspense>
          </div>
        )}

        {/* Connection Status Indicator */}
        {!isConnected && (
          <div className="fixed top-4 right-4 cyber-glass px-4 py-2 rounded-lg text-cyber-warning flex items-center gap-2 shadow-neon-cyan animate-pulse">
            <div className="w-2 h-2 bg-cyber-warning rounded-full animate-pulse"></div>
            <span className="font-display uppercase text-sm tracking-wide">Connexion API perdue</span>
          </div>
        )}
      </div>
    </ErrorBoundary>
  );
}

export default App;
