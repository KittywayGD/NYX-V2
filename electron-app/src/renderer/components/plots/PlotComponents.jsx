/**
 * Optimized Plotly Components
 * Reusable, memoized plot components
 */

import React, { memo, useMemo } from 'react';
import Plot from 'react-plotly.js';
import {
  PLOT_2D_LAYOUT,
  PLOT_3D_LAYOUT,
  PLOT_POLAR_LAYOUT,
  BASE_PLOT_CONFIG,
  MARKER_CONFIGS,
  PLOT_COLORS,
} from '../../utils/plotConfig';

/**
 * 2D Function Plot Component
 */
export const Plot2D = memo(({ data, plotRef }) => {
  const plotData = useMemo(() => {
    const traces = [
      {
        x: data.data.x,
        y: data.data.y,
        type: 'scatter',
        mode: 'lines',
        line: { color: PLOT_COLORS.primary, width: 2 },
        name: data.data.function,
      },
    ];

    // Add zeros
    if (data.metadata?.zeros?.length > 0) {
      traces.push({
        x: data.metadata.zeros,
        y: data.metadata.zeros.map(() => 0),
        type: 'scatter',
        mode: 'markers',
        marker: MARKER_CONFIGS.zeros,
        name: 'Zéros',
      });
    }

    // Add critical points
    if (data.metadata?.critical_points?.length > 0) {
      const mins = data.metadata.critical_points.filter((p) => p.type === 'minimum');
      const maxs = data.metadata.critical_points.filter((p) => p.type === 'maximum');

      if (mins.length > 0) {
        traces.push({
          x: mins.map((p) => p.x),
          y: mins.map((p) => p.y),
          type: 'scatter',
          mode: 'markers',
          marker: MARKER_CONFIGS.minimum,
          name: 'Minimums',
        });
      }

      if (maxs.length > 0) {
        traces.push({
          x: maxs.map((p) => p.x),
          y: maxs.map((p) => p.y),
          type: 'scatter',
          mode: 'markers',
          marker: MARKER_CONFIGS.maximum,
          name: 'Maximums',
        });
      }
    }

    return traces;
  }, [data]);

  return (
    <Plot
      data={plotData}
      layout={PLOT_2D_LAYOUT}
      config={BASE_PLOT_CONFIG}
      style={{ width: '100%', height: '500px' }}
      ref={plotRef}
    />
  );
});

Plot2D.displayName = 'Plot2D';

/**
 * 3D Surface Plot Component
 */
export const Plot3D = memo(({ data, plotRef }) => {
  const plotData = useMemo(() => [
    {
      x: data.data.x,
      y: data.data.y,
      z: data.data.z,
      type: 'surface',
      colorscale: 'Viridis',
      name: data.data.function,
    },
  ], [data]);

  return (
    <Plot
      data={plotData}
      layout={PLOT_3D_LAYOUT}
      config={BASE_PLOT_CONFIG}
      style={{ width: '100%', height: '500px' }}
      ref={plotRef}
    />
  );
});

Plot3D.displayName = 'Plot3D';

/**
 * Parametric Plot Component
 */
export const PlotParametric = memo(({ data, plotRef }) => {
  const plotData = useMemo(() => [
    {
      x: data.data.x,
      y: data.data.y,
      type: 'scatter',
      mode: 'lines',
      line: { color: PLOT_COLORS.primary, width: 2 },
      name: `(${data.data.x_expr}, ${data.data.y_expr})`,
    },
  ], [data]);

  const layout = useMemo(() => ({
    ...PLOT_2D_LAYOUT,
    yaxis: {
      ...PLOT_2D_LAYOUT.yaxis,
      scaleanchor: 'x',
    },
  }), []);

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={BASE_PLOT_CONFIG}
      style={{ width: '100%', height: '500px' }}
      ref={plotRef}
    />
  );
});

PlotParametric.displayName = 'PlotParametric';

/**
 * Polar Plot Component
 */
export const PlotPolar = memo(({ data, plotRef }) => {
  const plotData = useMemo(() => [
    {
      r: data.data.r,
      theta: data.data.theta.map((t) => (t * 180) / Math.PI), // Convert to degrees
      type: 'scatterpolar',
      mode: 'lines',
      line: { color: PLOT_COLORS.primary, width: 2 },
      name: data.data.r_expr,
    },
  ], [data]);

  return (
    <Plot
      data={plotData}
      layout={PLOT_POLAR_LAYOUT}
      config={BASE_PLOT_CONFIG}
      style={{ width: '100%', height: '500px' }}
      ref={plotRef}
    />
  );
});

PlotPolar.displayName = 'PlotPolar';

/**
 * Animation Plot Component
 */
export const PlotAnimation = memo(({ data, plotRef }) => {
  const [frameIndex, setFrameIndex] = React.useState(0);
  const [isPlaying, setIsPlaying] = React.useState(false);

  React.useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setFrameIndex((prev) => (prev + 1) % data.data.frames.length);
    }, 100);

    return () => clearInterval(interval);
  }, [isPlaying, data.data.frames.length]);

  const currentFrame = useMemo(
    () => data.data.frames[frameIndex],
    [data.data.frames, frameIndex]
  );

  const plotData = useMemo(() => [
    {
      x: currentFrame.x,
      y: currentFrame.y,
      type: 'scatter',
      mode: 'lines',
      line: { color: PLOT_COLORS.primary, width: 2 },
      name: `${data.data.parameter_name} = ${currentFrame.parameter_value.toFixed(2)}`,
    },
  ], [currentFrame, data.data.parameter_name]);

  return (
    <div>
      <Plot
        data={plotData}
        layout={PLOT_2D_LAYOUT}
        config={BASE_PLOT_CONFIG}
        style={{ width: '100%', height: '400px' }}
        ref={plotRef}
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
});

PlotAnimation.displayName = 'PlotAnimation';
