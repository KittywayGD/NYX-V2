import { Circle, Cpu, Zap } from 'lucide-react';
import useNyxStore from '../store/nyxStore';

function StatusBar() {
  const { isConnected, nyxStatus, isProcessing } = useNyxStore();

  return (
    <div className="glass px-4 py-2 border-t border-gray-700 flex items-center justify-between text-sm">
      {/* Left - Connection Status */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <Circle
            className={`w-2 h-2 ${
              isConnected ? 'text-nyx-success fill-current' : 'text-nyx-error fill-current'
            }`}
          />
          <span className="text-gray-400">
            {isConnected ? 'Connecté' : 'Déconnecté'}
          </span>
        </div>

        {nyxStatus && (
          <div className="text-gray-500">
            v{nyxStatus.nyx?.version || '2.0.0'}
          </div>
        )}
      </div>

      {/* Center - Processing Status */}
      {isProcessing && (
        <div className="flex items-center gap-2 text-nyx-accent">
          <Cpu className="w-4 h-4 animate-pulse" />
          <span>Traitement en cours...</span>
        </div>
      )}

      {/* Right - Modules Status */}
      <div className="flex items-center gap-3 text-gray-400">
        {nyxStatus?.sandboxes && (
          <>
            <StatusIndicator
              active={nyxStatus.sandboxes.math}
              label="Math"
            />
            <StatusIndicator
              active={nyxStatus.sandboxes.physics}
              label="Physique"
            />
            <StatusIndicator
              active={nyxStatus.sandboxes.electronics}
              label="Électronique"
            />
          </>
        )}
      </div>
    </div>
  );
}

function StatusIndicator({ active, label }) {
  return (
    <div className="flex items-center gap-1">
      <Zap className={`w-3 h-3 ${active ? 'text-nyx-success' : 'text-gray-600'}`} />
      <span className="text-xs">{label}</span>
    </div>
  );
}

export default StatusBar;
