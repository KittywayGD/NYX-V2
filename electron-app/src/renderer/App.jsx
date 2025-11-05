import { useEffect, useState } from 'react';
import useNyxStore from './store/nyxStore';
import ChatInterface from './components/ChatInterface';
import SandboxPanel from './components/SandboxPanel';
import Sidebar from './components/Sidebar';
import StatusBar from './components/StatusBar';
import { Activity } from 'lucide-react';

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
    <div className="flex h-screen bg-nyx-darker text-white overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {/* Chat Interface */}
        <div className={`flex-1 ${sandboxVisible ? 'w-1/2' : 'w-full'}`}>
          <ChatInterface />
        </div>

        {/* Status Bar */}
        <StatusBar />
      </div>

      {/* Sandbox Panel */}
      {sandboxVisible && (
        <div className="w-1/2 border-l border-gray-700">
          <SandboxPanel />
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
  );
}

export default App;
