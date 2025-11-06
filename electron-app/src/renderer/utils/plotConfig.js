/**
 * Plotly Configuration Constants
 * Centralized plot styling to reduce duplication across sandbox components
 */

// Dark theme colors
export const PLOT_COLORS = {
  background: '#1e293b',
  paper: '#1e293b',
  plot: '#0f172a',
  text: '#e2e8f0',
  grid: '#334155',
  zeroline: '#475569',
  primary: '#3b82f6',
  success: '#10b981',
  error: '#ef4444',
  warning: '#f59e0b',
};

// Base layout configuration for all plots
export const BASE_PLOT_LAYOUT = {
  paper_bgcolor: PLOT_COLORS.paper,
  plot_bgcolor: PLOT_COLORS.plot,
  font: { color: PLOT_COLORS.text },
  showlegend: true,
  legend: {
    x: 1,
    xanchor: 'right',
    y: 1,
  },
};

// 2D plot layout
export const PLOT_2D_LAYOUT = {
  ...BASE_PLOT_LAYOUT,
  xaxis: {
    title: 'x',
    gridcolor: PLOT_COLORS.grid,
    zerolinecolor: PLOT_COLORS.zeroline,
  },
  yaxis: {
    title: 'y',
    gridcolor: PLOT_COLORS.grid,
    zerolinecolor: PLOT_COLORS.zeroline,
  },
  margin: { l: 50, r: 50, t: 30, b: 50 },
};

// 3D plot layout
export const PLOT_3D_LAYOUT = {
  ...BASE_PLOT_LAYOUT,
  scene: {
    xaxis: {
      title: 'x',
      gridcolor: PLOT_COLORS.grid,
      backgroundcolor: PLOT_COLORS.plot,
    },
    yaxis: {
      title: 'y',
      gridcolor: PLOT_COLORS.grid,
      backgroundcolor: PLOT_COLORS.plot,
    },
    zaxis: {
      title: 'z',
      gridcolor: PLOT_COLORS.grid,
      backgroundcolor: PLOT_COLORS.plot,
    },
  },
  margin: { l: 0, r: 0, t: 30, b: 0 },
};

// Polar plot layout
export const PLOT_POLAR_LAYOUT = {
  ...BASE_PLOT_LAYOUT,
  polar: {
    bgcolor: PLOT_COLORS.plot,
    angularaxis: { gridcolor: PLOT_COLORS.grid },
    radialaxis: { gridcolor: PLOT_COLORS.grid },
  },
  margin: { l: 50, r: 50, t: 50, b: 50 },
};

// Base config for all Plotly instances
export const BASE_PLOT_CONFIG = {
  responsive: true,
  displayModeBar: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d'],
};

// Marker configurations
export const MARKER_CONFIGS = {
  zeros: {
    color: PLOT_COLORS.success,
    size: 8,
  },
  minimum: {
    color: PLOT_COLORS.primary,
    size: 10,
    symbol: 'triangle-down',
  },
  maximum: {
    color: PLOT_COLORS.error,
    size: 10,
    symbol: 'triangle-up',
  },
};

// Export image options
export const EXPORT_IMAGE_OPTIONS = {
  png: {
    format: 'png',
    width: 1200,
    height: 800,
  },
  svg: {
    format: 'svg',
    width: 1200,
    height: 800,
  },
};
