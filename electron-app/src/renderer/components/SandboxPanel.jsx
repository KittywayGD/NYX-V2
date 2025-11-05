import useNyxStore from '../store/nyxStore';
import { X, Maximize2 } from 'lucide-react';
import MathSandbox from './sandboxes/MathSandbox';
import PhysicsSandbox from './sandboxes/PhysicsSandbox';
import ElectronicsSandbox from './sandboxes/ElectronicsSandbox';

function SandboxPanel() {
  const { activeSandbox, sandboxData, closeSandbox } = useNyxStore();

  return (
    <div className="h-full flex flex-col bg-nyx-dark">
      {/* Header */}
      <div className="glass px-4 py-3 border-b border-gray-700 flex items-center justify-between">
        <div>
          <h3 className="font-semibold capitalize">{activeSandbox} Sandbox</h3>
          <p className="text-xs text-gray-400">Visualisation Interactive</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={closeSandbox}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
            title="Fermer le sandbox"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4">
        {activeSandbox === 'mathematics' && (
          <MathSandbox data={sandboxData} />
        )}
        {activeSandbox === 'physics' && (
          <PhysicsSandbox data={sandboxData} />
        )}
        {activeSandbox === 'electronics' && (
          <ElectronicsSandbox data={sandboxData} />
        )}
      </div>
    </div>
  );
}

export default SandboxPanel;
