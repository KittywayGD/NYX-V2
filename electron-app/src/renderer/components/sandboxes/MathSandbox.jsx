import { useEffect, useRef, useState } from 'react';
import Plot from 'react-plotly.js';
import useNyxStore from '../store/nyxStore';
import { X, Download, ZoomIn, ZoomOut, RotateCcw, Maximize2 } from 'lucide-react';

function MathSandbox({ data }) {
  const [plotData, setPlotData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const plotRef = useRef(null);

  useEffect(() => {
    loadPlotData();
  }, [data]);

  const loadPlotData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Extract function from query result
      let functionStr = null;
      let params = {};

      if (data?.result?.result?.function) {
        functionStr = data.result.result.function;
      } else if (data?.metadata?.parameters?.function) {
        functionStr = data.metadata.parameters.function;
      }

      if (!functionStr) {
        setError("Aucune fonction trouvée dans les résultats");
        return;
      }

      // Detect plot type from query
      const query = data.original_query || '';
      const queryLower = query.toLowerCase();

      let plotType = '2d';
      if (queryLower.includes('3d') || queryLower.includes('surface')) {
        plotType = '3d';
      } else if (queryLower.includes('paramétrique') || queryLower.includes('parametric')) {
        plotType = 'parametric';
      } else if (queryLower.includes('polaire') || queryLower.includes('polar')) {
        plotType = 'polar';
      }

      // Request plot data from API
      const result = await window.nyxAPI.mathPlot({
        function: functionStr,
        x_min: params.x_min || -10,
        x_max: params.x_max || 10,
        plot_type: plotType,
        parameters: params,
      });

      if (result.success) {
        setPlotData(result);
      } else {
        setError(result.error || "Erreur lors du traçage");
      }
    } catch (err) {
      console.error('Error loading plot:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const exportPlot = (format) => {
    if (!plotRef.current) return;

    const plotlyDiv = plotRef.current.el;

    if (format === 'png') {
      window.Plotly.downloadImage(plotlyDiv, {
        format: 'png',
        width: 1200,
        height: 800,
        filename: `nyx-plot-${Date.now()}`,
      });
    } else if (format === 'svg') {
      window.Plotly.downloadImage(plotlyDiv, {
        format: 'svg',
        width: 1200,
        height: 800,
        filename: `nyx-plot-${Date.now()}`,
      });
    } else if (format === 'json') {
      const dataStr = JSON.stringify(plotData, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `nyx-data-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const resetView = () => {
    if (plotRef.current?.el) {
      window.Plotly.relayout(plotRef.current.el, {
        'xaxis.autorange': true,
        'yaxis.autorange': true,
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Génération du graphique...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass p-4 rounded-lg border border-nyx-error">
        <p className="text-nyx-error">{error}</p>
        <button
          onClick={loadPlotData}
          className="mt-2 px-3 py-1 bg-nyx-accent rounded text-sm"
        >
          Réessayer
        </button>
      </div>
    );
  }

  if (!plotData?.data) {
    return <div className="text-gray-400">Aucune donnée à afficher</div>;
  }

  return (
    <div className="space-y-4">
      {/* Function Info */}
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <h4 className="font-semibold">Fonction</h4>
          <div className="flex gap-2">
            <button
              onClick={() => exportPlot('png')}
              className="p-2 hover:bg-gray-700 rounded transition-colors"
              title="Exporter en PNG"
            >
              <Download className="w-4 h-4" />
            </button>
            <button
              onClick={resetView}
              className="p-2 hover:bg-gray-700 rounded transition-colors"
              title="Réinitialiser la vue"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
        <code className="text-nyx-accent text-lg">
          {plotData.data.function}
        </code>
        <div className="mt-2 text-sm text-gray-400">
          Type: {plotData.type} • Points: {plotData.data.x?.length || 0}
        </div>
      </div>

      {/* Interactive Plot */}
      <div className="glass p-4 rounded-lg">
        {plotData.type === 'function_2d' && (
          <Plot2D data={plotData} ref={plotRef} />
        )}
        {plotData.type === 'function_3d' && (
          <Plot3D data={plotData} ref={plotRef} />
        )}
        {plotData.type === 'parametric_2d' && (
          <PlotParametric data={plotData} ref={plotRef} />
        )}
        {plotData.type === 'polar' && (
          <PlotPolar data={plotData} ref={plotRef} />
        )}
        {plotData.type === 'animation' && (
          <PlotAnimation data={plotData} ref={plotRef} />
        )}
      </div>

      {/* Analysis */}
      {plotData.metadata && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Analyse</h4>
          <div className="space-y-2 text-sm">
            {/* Zeros */}
            {plotData.metadata.zeros?.length > 0 && (
              <div>
                <span className="text-gray-400">Zéros:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {plotData.metadata.zeros.map((zero, i) => (
                    <span key={i} className="px-2 py-1 bg-nyx-dark rounded">
                      x = {zero.toFixed(3)}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Critical Points */}
            {plotData.metadata.critical_points?.length > 0 && (
              <div>
                <span className="text-gray-400">Points critiques:</span>
                <div className="space-y-1 mt-1">
                  {plotData.metadata.critical_points.map((point, i) => (
                    <div key={i} className="px-2 py-1 bg-nyx-dark rounded">
                      <span className={`font-semibold ${
                        point.type === 'minimum' ? 'text-blue-400' :
                        point.type === 'maximum' ? 'text-red-400' :
                        'text-yellow-400'
                      }`}>
                        {point.type === 'minimum' ? '↓ Min' :
                         point.type === 'maximum' ? '↑ Max' :
                         '○ Inflexion'}
                      </span>
                      {' '} ({point.x.toFixed(3)}, {point.y.toFixed(3)})
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Export Options */}
      <div className="glass p-3 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-400">Exporter:</span>
          <div className="flex gap-2">
            <button
              onClick={() => exportPlot('png')}
              className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            >
              PNG
            </button>
            <button
              onClick={() => exportPlot('svg')}
              className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            >
              SVG
            </button>
            <button
              onClick={() => exportPlot('json')}
              className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            >
              JSON
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Plot 2D Component
const Plot2D = ({ data, ref }) => {
  const plotData = [{
    x: data.data.x,
    y: data.data.y,
    type: 'scatter',
    mode: 'lines',
    line: { color: '#3b82f6', width: 2 },
    name: data.data.function,
  }];

  // Add zeros
  if (data.metadata?.zeros?.length > 0) {
    plotData.push({
      x: data.metadata.zeros,
      y: data.metadata.zeros.map(() => 0),
      type: 'scatter',
      mode: 'markers',
      marker: { color: '#10b981', size: 8 },
      name: 'Zéros',
    });
  }

  // Add critical points
  if (data.metadata?.critical_points?.length > 0) {
    const mins = data.metadata.critical_points.filter(p => p.type === 'minimum');
    const maxs = data.metadata.critical_points.filter(p => p.type === 'maximum');

    if (mins.length > 0) {
      plotData.push({
        x: mins.map(p => p.x),
        y: mins.map(p => p.y),
        type: 'scatter',
        mode: 'markers',
        marker: { color: '#3b82f6', size: 10, symbol: 'triangle-down' },
        name: 'Minimums',
      });
    }

    if (maxs.length > 0) {
      plotData.push({
        x: maxs.map(p => p.x),
        y: maxs.map(p => p.y),
        type: 'scatter',
        mode: 'markers',
        marker: { color: '#ef4444', size: 10, symbol: 'triangle-up' },
        name: 'Maximums',
      });
    }
  }

  const layout = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#0f172a',
    font: { color: '#e2e8f0' },
    xaxis: {
      title: 'x',
      gridcolor: '#334155',
      zerolinecolor: '#475569',
    },
    yaxis: {
      title: 'y',
      gridcolor: '#334155',
      zerolinecolor: '#475569',
    },
    showlegend: true,
    legend: {
      x: 1,
      xanchor: 'right',
      y: 1,
    },
    margin: { l: 50, r: 50, t: 30, b: 50 },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '500px' }}
      ref={ref}
    />
  );
};

// Plot 3D Component
const Plot3D = ({ data, ref }) => {
  const plotData = [{
    x: data.data.x,
    y: data.data.y,
    z: data.data.z,
    type: 'surface',
    colorscale: 'Viridis',
    name: data.data.function,
  }];

  const layout = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#0f172a',
    font: { color: '#e2e8f0' },
    scene: {
      xaxis: { title: 'x', gridcolor: '#334155', backgroundcolor: '#0f172a' },
      yaxis: { title: 'y', gridcolor: '#334155', backgroundcolor: '#0f172a' },
      zaxis: { title: 'z', gridcolor: '#334155', backgroundcolor: '#0f172a' },
    },
    margin: { l: 0, r: 0, t: 30, b: 0 },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '500px' }}
      ref={ref}
    />
  );
};

// Parametric Plot Component
const PlotParametric = ({ data, ref }) => {
  const plotData = [{
    x: data.data.x,
    y: data.data.y,
    type: 'scatter',
    mode: 'lines',
    line: { color: '#3b82f6', width: 2 },
    name: `(${data.data.x_expr}, ${data.data.y_expr})`,
  }];

  const layout = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#0f172a',
    font: { color: '#e2e8f0' },
    xaxis: { title: 'x', gridcolor: '#334155', zerolinecolor: '#475569' },
    yaxis: { title: 'y', gridcolor: '#334155', zerolinecolor: '#475569', scaleanchor: 'x' },
    showlegend: true,
    margin: { l: 50, r: 50, t: 30, b: 50 },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '500px' }}
      ref={ref}
    />
  );
};

// Polar Plot Component
const PlotPolar = ({ data, ref }) => {
  const plotData = [{
    r: data.data.r,
    theta: data.data.theta.map(t => t * 180 / Math.PI), // Convert to degrees
    type: 'scatterpolar',
    mode: 'lines',
    line: { color: '#3b82f6', width: 2 },
    name: data.data.r_expr,
  }];

  const layout = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#0f172a',
    font: { color: '#e2e8f0' },
    polar: {
      bgcolor: '#0f172a',
      angularaxis: { gridcolor: '#334155' },
      radialaxis: { gridcolor: '#334155' },
    },
    showlegend: true,
    margin: { l: 50, r: 50, t: 50, b: 50 },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={config}
      style={{ width: '100%', height: '500px' }}
      ref={ref}
    />
  );
};

// Animation Component
const PlotAnimation = ({ data, ref }) => {
  const [frameIndex, setFrameIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setFrameIndex(prev => (prev + 1) % data.data.frames.length);
    }, 100);

    return () => clearInterval(interval);
  }, [isPlaying, data.data.frames.length]);

  const currentFrame = data.data.frames[frameIndex];

  const plotData = [{
    x: currentFrame.x,
    y: currentFrame.y,
    type: 'scatter',
    mode: 'lines',
    line: { color: '#3b82f6', width: 2 },
    name: `${data.data.parameter_name} = ${currentFrame.parameter_value.toFixed(2)}`,
  }];

  const layout = {
    paper_bgcolor: '#1e293b',
    plot_bgcolor: '#0f172a',
    font: { color: '#e2e8f0' },
    xaxis: { title: 'x', gridcolor: '#334155', zerolinecolor: '#475569' },
    yaxis: { title: 'y', gridcolor: '#334155', zerolinecolor: '#475569' },
    showlegend: true,
    margin: { l: 50, r: 50, t: 30, b: 50 },
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
  };

  return (
    <div>
      <Plot
        data={plotData}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '400px' }}
        ref={ref}
      />
      <div className="mt-3 flex items-center gap-3">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="px-4 py-2 bg-nyx-accent hover:bg-nyx-accent-hover rounded transition-colors"
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <input
          type="range"
          min="0"
          max={data.data.frames.length - 1}
          value={frameIndex}
          onChange={(e) => setFrameIndex(parseInt(e.target.value))}
          className="flex-1"
        />
        <span className="text-sm text-gray-400">
          Frame {frameIndex + 1}/{data.data.frames.length}
        </span>
      </div>
    </div>
  );
};

export default MathSandbox;
