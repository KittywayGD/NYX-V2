import { Circle, Cpu, Zap, Activity } from 'lucide-react';
import useNyxStore from '../store/nyxStore';

function StatusBar() {
  const { isConnected, nyxStatus, isProcessing } = useNyxStore();

  return (
    <div className="cyber-glass px-6 py-3 border-t border-cyber-cyan border-opacity-20 flex items-center justify-between text-sm font-display">
      {/* Left - Connection Status */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Circle
            className={`w-2.5 h-2.5 ${
              isConnected ? 'text-cyber-success fill-current animate-pulse' : 'text-cyber-error fill-current'
            }`}
          />
          <span className={`uppercase tracking-wide ${isConnected ? 'text-cyber-success' : 'text-cyber-error'}`}>
            {isConnected ? 'Online' : 'Offline'}
          </span>
        </div>

        {nyxStatus && (
          <div className="text-cyber-cyan text-opacity-60 uppercase text-xs tracking-wider">
            v{nyxStatus.nyx?.version || '2.0.0'}
          </div>
        )}
      </div>

      {/* Center - Processing Status */}
      {isProcessing && (
        <div className="flex items-center gap-2 text-cyber-cyan animate-pulse">
          <Activity className="w-4 h-4 animate-spin" style={{ filter: 'drop-shadow(0 0 6px rgba(6, 182, 212, 0.8))' }} />
          <span className="uppercase tracking-wide text-xs">Processing...</span>
        </div>
      )}

      {/* Right - Modules Status */}
      <div className="flex items-center gap-4 text-cyber-cyan text-opacity-70">
        {nyxStatus?.sandboxes && (
          <>
            <StatusIndicator
              active={nyxStatus.sandboxes.math}
              label="MATH"
              color="purple"
            />
            <StatusIndicator
              active={nyxStatus.sandboxes.physics}
              label="PHY"
              color="cyan"
            />
            <StatusIndicator
              active={nyxStatus.sandboxes.electronics}
              label="ELEC"
              color="pink"
            />
          </>
        )}
      </div>
    </div>
  );
}

function StatusIndicator({ active, label, color = 'cyan' }) {
  const colors = {
    cyan: active ? 'text-cyber-cyan' : 'text-cyber-cyan text-opacity-30',
    purple: active ? 'text-cyber-purple' : 'text-cyber-purple text-opacity-30',
    pink: active ? 'text-cyber-pink' : 'text-cyber-pink text-opacity-30',
  };

  return (
    <div className={`flex items-center gap-1.5 transition-all duration-300 ${colors[color]}`}>
      <Zap className={`w-3.5 h-3.5 ${active ? 'animate-pulse' : ''}`} style={active ? { filter: `drop-shadow(0 0 4px currentColor)` } : {}} />
      <span className="text-xs uppercase tracking-wider font-semibold">{label}</span>
    </div>
  );
}

export default StatusBar;
