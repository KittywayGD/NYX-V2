import { useEffect, useState, useRef } from 'react';
import Plot from 'react-plotly.js';
import { Play, Pause, Download, Plus, Trash2, Zap } from 'lucide-react';

function ElectronicsSandbox({ data }) {
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [circuitType, setCircuitType] = useState(null);

  useEffect(() => {
    loadSimulation();
  }, [data]);

  const loadSimulation = async () => {
    try {
      setLoading(true);
      const query = data?.original_query || '';
      const queryLower = query.toLowerCase();

      let type = 'rc';
      if (queryLower.includes('rl') && !queryLower.includes('rlc')) {
        type = 'rl';
      } else if (queryLower.includes('rlc')) {
        type = 'rlc';
      } else if (queryLower.includes('diviseur') || queryLower.includes('divider')) {
        type = 'divider';
      }

      setCircuitType(type);

      const params = {
        resistance: 1000,
        capacitance: 1e-6,
        inductance: 0.1,
        voltage: 5,
      };

      const result = await window.nyxAPI.electronicsSimulate({
        circuit_type: type,
        parameters: params,
      });

      if (result.success) {
        setSimulationData(result);
      }
    } catch (err) {
      console.error('Error loading simulation:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-gray-400">Chargement de la simulation...</div>;
  }

  if (!simulationData) {
    return <div className="text-gray-400">Aucune donnée de simulation</div>;
  }

  return (
    <div className="space-y-4">
      {circuitType === 'rc' && <RCCircuitView data={simulationData} />}
      {circuitType === 'rl' && <RLCircuitView data={simulationData} />}
      {circuitType === 'rlc' && <RLCCircuitView data={simulationData} />}
      {circuitType === 'divider' && <VoltageDividerView data={simulationData} />}
    </div>
  );
}

// Circuit Drawer Component
function CircuitDrawer({ components, onUpdate }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set dark background
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 0.5;
    for (let x = 0; x < canvas.width; x += 20) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 20) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }

    // Draw components
    components.forEach(comp => {
      drawComponent(ctx, comp);
    });
  }, [components]);

  const drawComponent = (ctx, comp) => {
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 2;
    ctx.font = '12px sans-serif';
    ctx.fillStyle = '#e2e8f0';

    const { x, y, type, value, orientation = 'horizontal' } = comp;

    switch (type) {
      case 'resistor':
        drawResistor(ctx, x, y, orientation);
        ctx.fillText(`R: ${formatValue(value, 'Ω')}`, x + 10, y - 10);
        break;
      case 'capacitor':
        drawCapacitor(ctx, x, y, orientation);
        ctx.fillText(`C: ${formatValue(value, 'F')}`, x + 10, y - 10);
        break;
      case 'inductor':
        drawInductor(ctx, x, y, orientation);
        ctx.fillText(`L: ${formatValue(value, 'H')}`, x + 10, y - 10);
        break;
      case 'voltage_source':
        drawVoltageSource(ctx, x, y);
        ctx.fillText(`V: ${value}V`, x + 10, y - 10);
        break;
      case 'ground':
        drawGround(ctx, x, y);
        break;
      case 'wire':
        drawWire(ctx, x, y, comp.x2, comp.y2);
        break;
    }
  };

  const drawResistor = (ctx, x, y, orientation) => {
    ctx.beginPath();
    if (orientation === 'horizontal') {
      ctx.moveTo(x, y);
      ctx.lineTo(x + 10, y);
      ctx.lineTo(x + 15, y - 10);
      ctx.lineTo(x + 25, y + 10);
      ctx.lineTo(x + 35, y - 10);
      ctx.lineTo(x + 45, y + 10);
      ctx.lineTo(x + 50, y);
      ctx.lineTo(x + 60, y);
    } else {
      ctx.moveTo(x, y);
      ctx.lineTo(x, y + 10);
      ctx.lineTo(x - 10, y + 15);
      ctx.lineTo(x + 10, y + 25);
      ctx.lineTo(x - 10, y + 35);
      ctx.lineTo(x + 10, y + 45);
      ctx.lineTo(x, y + 50);
      ctx.lineTo(x, y + 60);
    }
    ctx.stroke();
  };

  const drawCapacitor = (ctx, x, y, orientation) => {
    ctx.beginPath();
    if (orientation === 'horizontal') {
      ctx.moveTo(x, y);
      ctx.lineTo(x + 25, y);
      ctx.moveTo(x + 25, y - 15);
      ctx.lineTo(x + 25, y + 15);
      ctx.moveTo(x + 35, y - 15);
      ctx.lineTo(x + 35, y + 15);
      ctx.moveTo(x + 35, y);
      ctx.lineTo(x + 60, y);
    } else {
      ctx.moveTo(x, y);
      ctx.lineTo(x, y + 25);
      ctx.moveTo(x - 15, y + 25);
      ctx.lineTo(x + 15, y + 25);
      ctx.moveTo(x - 15, y + 35);
      ctx.lineTo(x + 15, y + 35);
      ctx.moveTo(x, y + 35);
      ctx.lineTo(x, y + 60);
    }
    ctx.stroke();
  };

  const drawInductor = (ctx, x, y, orientation) => {
    ctx.beginPath();
    if (orientation === 'horizontal') {
      ctx.moveTo(x, y);
      ctx.lineTo(x + 10, y);
      for (let i = 0; i < 4; i++) {
        ctx.arc(x + 15 + i * 10, y, 5, Math.PI, 0, false);
      }
      ctx.lineTo(x + 60, y);
    }
    ctx.stroke();
  };

  const drawVoltageSource = (ctx, x, y) => {
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.fillText('+', x - 5, y - 5);
    ctx.fillText('-', x - 5, y + 10);
  };

  const drawGround = (ctx, x, y) => {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y + 10);
    ctx.moveTo(x - 15, y + 10);
    ctx.lineTo(x + 15, y + 10);
    ctx.moveTo(x - 10, y + 15);
    ctx.lineTo(x + 10, y + 15);
    ctx.moveTo(x - 5, y + 20);
    ctx.lineTo(x + 5, y + 20);
    ctx.stroke();
  };

  const drawWire = (ctx, x1, y1, x2, y2) => {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  };

  const formatValue = (value, unit) => {
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M${unit}`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}k${unit}`;
    if (value >= 1) return `${value.toFixed(1)}${unit}`;
    if (value >= 1e-3) return `${(value * 1e3).toFixed(1)}m${unit}`;
    if (value >= 1e-6) return `${(value * 1e6).toFixed(1)}µ${unit}`;
    if (value >= 1e-9) return `${(value * 1e9).toFixed(1)}n${unit}`;
    return `${value}${unit}`;
  };

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={600}
        height={400}
        className="w-full rounded border border-gray-700"
      />
    </div>
  );
}

// RC Circuit View
function RCCircuitView({ data }) {
  const exportData = () => {
    const dataStr = JSON.stringify(data, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rc-circuit-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Create circuit components
  const components = [
    { type: 'voltage_source', x: 50, y: 100, value: data.parameters.voltage },
    { type: 'wire', x: 70, y: 100, x2: 150, y2: 100 },
    { type: 'resistor', x: 150, y: 100, value: data.parameters.resistance, orientation: 'horizontal' },
    { type: 'wire', x: 210, y: 100, x2: 300, y2: 100 },
    { type: 'capacitor', x: 300, y: 100, value: data.parameters.capacitance, orientation: 'vertical' },
    { type: 'wire', x: 300, y: 160, x2: 300, y2: 250 },
    { type: 'wire', x: 300, y: 250, x2: 50, y2: 250 },
    { type: 'wire', x: 50, y: 250, x2: 50, y2: 120 },
    { type: 'ground', x: 50, y: 250 },
  ];

  return (
    <div className="space-y-4">
      {/* Circuit Diagram */}
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold">Circuit RC</h4>
          <button
            onClick={exportData}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
        <CircuitDrawer components={components} />
      </div>

      {/* Voltage Plot */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Tension du Condensateur</h4>
          <Plot
            data={[{
              x: data.data.time,
              y: data.data.voltage_capacitor,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#3b82f6', width: 2 },
              name: 'Vc(t)',
            }]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Tension (V)', gridcolor: '#334155' },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Current Plot */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Courant</h4>
          <Plot
            data={[{
              x: data.data.time,
              y: data.data.current,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#10b981', width: 2 },
              name: 'I(t)',
            }]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Courant (A)', gridcolor: '#334155' },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Analysis */}
      {data.analysis && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Analyse</h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Constante de temps τ</div>
              <div className="text-lg font-semibold">{(data.analysis.time_constant * 1000).toFixed(2)} ms</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Temps à 63%</div>
              <div className="text-lg font-semibold">{(data.analysis.time_to_63_percent * 1000).toFixed(2)} ms</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Temps à 95%</div>
              <div className="text-lg font-semibold">{(data.analysis.time_to_95_percent * 1000).toFixed(2)} ms</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Courant max</div>
              <div className="text-lg font-semibold">{(data.analysis.max_current * 1000).toFixed(2)} mA</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// RL Circuit View (similar structure)
function RLCircuitView({ data }) {
  const components = [
    { type: 'voltage_source', x: 50, y: 100, value: data.parameters.voltage },
    { type: 'wire', x: 70, y: 100, x2: 150, y2: 100 },
    { type: 'resistor', x: 150, y: 100, value: data.parameters.resistance },
    { type: 'wire', x: 210, y: 100, x2: 300, y2: 100 },
    { type: 'inductor', x: 300, y: 100, value: data.parameters.inductance, orientation: 'vertical' },
    { type: 'wire', x: 300, y: 160, x2: 50, y2: 160 },
    { type: 'wire', x: 50, y: 160, x2: 50, y2: 120 },
  ];

  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-3">Circuit RL</h4>
        <CircuitDrawer components={components} />
      </div>
      {/* Similar plots as RC */}
    </div>
  );
}

// RLC Circuit View
function RLCCircuitView({ data }) {
  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-3">Circuit RLC Série</h4>
        <div className="mb-3 px-3 py-2 bg-nyx-dark rounded">
          <span className="text-sm text-gray-400">Régime: </span>
          <span className="font-semibold">{data.parameters.regime}</span>
        </div>
      </div>

      {/* Current Plot */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Courant</h4>
          <Plot
            data={[{
              x: data.data.time,
              y: data.data.current,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#3b82f6', width: 2 },
            }]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Courant (A)', gridcolor: '#334155' },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Voltages */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Tensions</h4>
          <Plot
            data={[
              {
                x: data.data.time,
                y: data.data.voltage_resistor,
                name: 'VR',
                line: { color: '#ef4444' },
              },
              {
                x: data.data.time,
                y: data.data.voltage_capacitor,
                name: 'VC',
                line: { color: '#3b82f6' },
              },
              {
                x: data.data.time,
                y: data.data.voltage_inductor,
                name: 'VL',
                line: { color: '#10b981' },
              },
            ]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Tension (V)', gridcolor: '#334155' },
              legend: { x: 1, xanchor: 'right', y: 1 },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Analysis */}
      {data.analysis && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Analyse</h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Fréquence naturelle</div>
              <div className="text-lg font-semibold">{data.analysis.resonant_frequency?.toFixed(2)} Hz</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Facteur de qualité</div>
              <div className="text-lg font-semibold">{data.analysis.quality_factor?.toFixed(2)}</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Coefficient d'amortissement</div>
              <div className="text-lg font-semibold">{data.analysis.damping_ratio?.toFixed(3)}</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Régime</div>
              <div className="text-lg font-semibold">{data.analysis.regime}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Voltage Divider View
function VoltageDividerView({ data }) {
  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <h4 className="font-semibold mb-3">Diviseur de Tension</h4>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="p-2 bg-nyx-dark rounded">
            <div className="text-gray-400">V_out</div>
            <div className="text-lg font-semibold">{data.data.v_out.toFixed(2)} V</div>
          </div>
          <div className="p-2 bg-nyx-dark rounded">
            <div className="text-gray-400">Courant</div>
            <div className="text-lg font-semibold">{(data.data.current * 1000).toFixed(2)} mA</div>
          </div>
          <div className="p-2 bg-nyx-dark rounded">
            <div className="text-gray-400">Ratio</div>
            <div className="text-lg font-semibold">{data.analysis.voltage_ratio.toFixed(3)}</div>
          </div>
          <div className="p-2 bg-nyx-dark rounded">
            <div className="text-gray-400">Atténuation</div>
            <div className="text-lg font-semibold">{data.analysis.attenuation_db.toFixed(1)} dB</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ElectronicsSandbox;
