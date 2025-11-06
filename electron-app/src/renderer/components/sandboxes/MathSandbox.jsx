/**
 * Math Sandbox Component - OPTIMIZED
 * Interactive mathematical visualization using Plotly
 */

import React, { memo, useRef } from 'react';
import { useAsyncData, usePlotExport } from '../../utils/hooks';
import {
  Plot2D,
  Plot3D,
  PlotParametric,
  PlotPolar,
  PlotAnimation,
} from '../plots/PlotComponents';
import {
  PlotToolbar,
  FunctionInfo,
  PlotAnalysis,
  ExportOptions,
  PlotLoading,
  PlotError,
} from '../plots/PlotControls';

const MathSandbox = memo(({ data }) => {
  const plotRef = useRef(null);
  const { data: plotData, loading, error, execute } = useAsyncData(null);
  const { exportPlot, resetView } = usePlotExport(plotRef);

  // Load plot data on mount or data change
  React.useEffect(() => {
    loadPlotData();
  }, [data]);

  const loadPlotData = async () => {
    await execute(async () => {
      // Extract function from query result
      let functionStr = null;
      let params = {};

      if (data?.result?.result?.function) {
        functionStr = data.result.result.function;
      } else if (data?.metadata?.parameters?.function) {
        functionStr = data.metadata.parameters.function;
      }

      if (!functionStr) {
        throw new Error('Aucune fonction trouvée dans les résultats');
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

      if (!result.success) {
        throw new Error(result.error || 'Erreur lors du traçage');
      }

      return result;
    });
  };

  // Render loading state
  if (loading) {
    return <PlotLoading />;
  }

  // Render error state
  if (error) {
    return <PlotError error={error} onRetry={loadPlotData} />;
  }

  // Render empty state
  if (!plotData?.data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Aucune donnée à afficher</div>
      </div>
    );
  }

  // Render plot based on type
  return (
    <div className="space-y-4">
      {/* Function Info */}
      <FunctionInfo
        functionStr={plotData.data.function}
        type={plotData.type}
        pointCount={plotData.data.x?.length || 0}
      >
        <PlotToolbar onExport={exportPlot} onReset={resetView} />
      </FunctionInfo>

      {/* Interactive Plot */}
      <div className="glass p-4 rounded-lg">
        {plotData.type === 'function_2d' && <Plot2D data={plotData} plotRef={plotRef} />}
        {plotData.type === 'function_3d' && <Plot3D data={plotData} plotRef={plotRef} />}
        {plotData.type === 'parametric_2d' && (
          <PlotParametric data={plotData} plotRef={plotRef} />
        )}
        {plotData.type === 'polar' && <PlotPolar data={plotData} plotRef={plotRef} />}
        {plotData.type === 'animation' && <PlotAnimation data={plotData} plotRef={plotRef} />}
      </div>

      {/* Analysis */}
      <PlotAnalysis metadata={plotData.metadata} />

      {/* Export Options */}
      <ExportOptions onExport={exportPlot} />
    </div>
  );
});

MathSandbox.displayName = 'MathSandbox';

export default MathSandbox;
