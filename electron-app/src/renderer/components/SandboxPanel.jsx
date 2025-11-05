import useNyxStore from '../store/nyxStore';
import { X, Maximize2 } from 'lucide-react';
import { useEffect, useState } from 'react';

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
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4">
        {activeSandbox === 'mathematics' && (
          <MathSandboxView data={sandboxData} />
        )}
        {activeSandbox === 'physics' && (
          <PhysicsSandboxView data={sandboxData} />
        )}
        {activeSandbox === 'electronics' && (
          <ElectronicsSandboxView data={sandboxData} />
        )}
      </div>
    </div>
  );
}

function MathSandboxView({ data }) {
  const [plotData, setPlotData] = useState(null);

  useEffect(() => {
    // Extract function from result
    if (data?.result?.result?.function) {
      const func = data.result.result.function;
      // Request plot data
      window.nyxAPI.mathPlot({
        function: func,
        x_min: -10,
        x_max: 10,
        plot_type: '2d',
      }).then(result => {
        if (result.success) {
          setPlotData(result);
        }
      });
    }
  }, [data]);

  if (!plotData?.data) {
    return <div className="text-gray-400">Chargement...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-2">Fonction</h4>
        <code className="text-nyx-accent">{plotData.data.function}</code>
      </div>

      {/* Plot Preview (simplified - would use Plotly in real app) */}
      <div className="glass p-4 rounded-lg">
        <div className="aspect-video bg-nyx-darker rounded flex items-center justify-center">
          <div className="text-center text-gray-400">
            <p className="mb-2">Graphique: {plotData.data.function}</p>
            <p className="text-sm">Intervalle: [{plotData.data.x_min}, {plotData.data.x_max}]</p>
            <p className="text-xs mt-2">{plotData.data.x.length} points</p>
          </div>
        </div>
      </div>

      {/* Analysis */}
      {plotData.metadata && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-2">Analyse</h4>
          <div className="space-y-1 text-sm">
            {plotData.metadata.zeros?.length > 0 && (
              <p>Zéros: {plotData.metadata.zeros.map(z => z.toFixed(2)).join(', ')}</p>
            )}
            {plotData.metadata.critical_points?.length > 0 && (
              <p>Points critiques: {plotData.metadata.critical_points.length}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function PhysicsSandboxView({ data }) {
  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-2">Simulation Physique</h4>
        <div className="aspect-video bg-nyx-darker rounded flex items-center justify-center">
          <p className="text-gray-400">Canvas de simulation</p>
        </div>
      </div>
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-2">Paramètres</h4>
        <pre className="text-xs overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
}

function ElectronicsSandboxView({ data }) {
  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-2">Circuit Électronique</h4>
        <div className="aspect-video bg-nyx-darker rounded flex items-center justify-center">
          <p className="text-gray-400">Schéma de circuit</p>
        </div>
      </div>
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-2">Résultats</h4>
        <pre className="text-xs overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
}

export default SandboxPanel;
