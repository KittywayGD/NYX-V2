import { useEffect, useState, lazy, Suspense } from 'react';
import useNyxStore from './store/nyxStore';
import ErrorBoundary from './components/ErrorBoundary';
import { Activity } from 'lucide-react';

// Lazy load heavy components
const ChatInterface = lazy(() => import('./components/ChatInterface'));
const SandboxPanel = lazy(() => import('./components/SandboxPanel'));
const Sidebar = lazy(() => import('./components/Sidebar'));
const StatusBar = lazy(() => import('./components/StatusBar'));

// Loading fallback component
const LoadingFallback = ({ message = 'Chargement...' }) => (
  <div className="flex items-center justify-center h-full">
    <div className="text-center">
      <Activity className="w-8 h-8 text-nyx-accent animate-spin mx-auto mb-2" />
      <p className="text-gray-400 text-sm">{message}</p>
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
      <div className="min-h-screen bg-nyx-darker flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-12 h-12 text-nyx-accent animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Initialisation de NYX-V2...</p>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="flex h-screen bg-nyx-darker text-white overflow-hidden">
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
          <div className="w-1/2 border-l border-gray-700">
            <Suspense fallback={<LoadingFallback message="Chargement sandbox..." />}>
              <SandboxPanel />
            </Suspense>
          </div>
        )}

        {/* Connection Status Indicator */}
        {!isConnected && (
          <div className="fixed top-4 right-4 glass px-4 py-2 rounded-lg text-nyx-warning flex items-center gap-2">
            <div className="w-2 h-2 bg-nyx-warning rounded-full animate-pulse"></div>
            <span>Connexion API perdue</span>
          </div>
        )}
      </div>
    </ErrorBoundary>
  );
}

export default App;
