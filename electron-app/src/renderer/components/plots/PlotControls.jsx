/**
 * Plot Control Components
 * Reusable UI controls for plot manipulation
 */

import React, { memo } from 'react';
import { Download, RotateCcw, X } from 'lucide-react';

/**
 * Plot Toolbar Component
 */
export const PlotToolbar = memo(({ onExport, onReset, onClose }) => {
  return (
    <div className="flex gap-2">
      {onExport && (
        <button
          onClick={() => onExport('png')}
          className="p-2 hover:bg-gray-700 rounded transition-colors"
          title="Exporter en PNG"
          aria-label="Export plot as PNG"
        >
          <Download className="w-4 h-4" />
        </button>
      )}
      {onReset && (
        <button
          onClick={onReset}
          className="p-2 hover:bg-gray-700 rounded transition-colors"
          title="Réinitialiser la vue"
          aria-label="Reset plot view"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      )}
      {onClose && (
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-700 rounded transition-colors"
          title="Fermer"
          aria-label="Close plot"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
});

PlotToolbar.displayName = 'PlotToolbar';

/**
 * Function Info Display
 */
export const FunctionInfo = memo(({ functionStr, type, pointCount, children }) => {
  return (
    <div className="glass p-4 rounded-lg">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold">Fonction</h4>
        {children}
      </div>
      <code className="text-nyx-accent text-lg block break-all">
        {functionStr}
      </code>
      {(type || pointCount) && (
        <div className="mt-2 text-sm text-gray-400">
          {type && <span>Type: {type}</span>}
          {type && pointCount && <span> • </span>}
          {pointCount && <span>Points: {pointCount}</span>}
        </div>
      )}
    </div>
  );
});

FunctionInfo.displayName = 'FunctionInfo';

/**
 * Plot Analysis Display
 */
export const PlotAnalysis = memo(({ metadata }) => {
  if (!metadata) return null;

  const { zeros, critical_points } = metadata;

  if (!zeros?.length && !critical_points?.length) return null;

  return (
    <div className="glass p-4 rounded-lg">
      <h4 className="font-semibold mb-3">Analyse</h4>
      <div className="space-y-2 text-sm">
        {/* Zeros */}
        {zeros?.length > 0 && (
          <div>
            <span className="text-gray-400">Zéros:</span>
            <div className="flex flex-wrap gap-2 mt-1">
              {zeros.map((zero, i) => (
                <span key={i} className="px-2 py-1 bg-nyx-dark rounded">
                  x = {zero.toFixed(3)}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Critical Points */}
        {critical_points?.length > 0 && (
          <div>
            <span className="text-gray-400">Points critiques:</span>
            <div className="space-y-1 mt-1">
              {critical_points.map((point, i) => (
                <div key={i} className="px-2 py-1 bg-nyx-dark rounded">
                  <span
                    className={`font-semibold ${
                      point.type === 'minimum'
                        ? 'text-blue-400'
                        : point.type === 'maximum'
                        ? 'text-red-400'
                        : 'text-yellow-400'
                    }`}
                  >
                    {point.type === 'minimum'
                      ? '↓ Min'
                      : point.type === 'maximum'
                      ? '↑ Max'
                      : '○ Inflexion'}
                  </span>
                  {' '}
                  ({point.x.toFixed(3)}, {point.y.toFixed(3)})
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
});

PlotAnalysis.displayName = 'PlotAnalysis';

/**
 * Export Options Component
 */
export const ExportOptions = memo(({ onExport }) => {
  return (
    <div className="glass p-3 rounded-lg">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-400">Exporter:</span>
        <div className="flex gap-2">
          <button
            onClick={() => onExport('png')}
            className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            aria-label="Export as PNG"
          >
            PNG
          </button>
          <button
            onClick={() => onExport('svg')}
            className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            aria-label="Export as SVG"
          >
            SVG
          </button>
          <button
            onClick={() => onExport('json')}
            className="px-3 py-1 bg-nyx-dark hover:bg-gray-700 rounded text-sm transition-colors"
            aria-label="Export as JSON"
          >
            JSON
          </button>
        </div>
      </div>
    </div>
  );
});

ExportOptions.displayName = 'ExportOptions';

/**
 * Loading State Component
 */
export const PlotLoading = memo(({ message = 'Génération du graphique...' }) => {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-400">{message}</div>
    </div>
  );
});

PlotLoading.displayName = 'PlotLoading';

/**
 * Error State Component
 */
export const PlotError = memo(({ error, onRetry }) => {
  return (
    <div className="glass p-4 rounded-lg border border-nyx-error">
      <p className="text-nyx-error">{error}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 px-3 py-1 bg-nyx-accent rounded text-sm hover:bg-nyx-accent-hover transition-colors"
        >
          Réessayer
        </button>
      )}
    </div>
  );
});

PlotError.displayName = 'PlotError';
