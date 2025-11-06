/**
 * Custom React Hooks
 * Reusable hooks for common patterns across components
 */

import { useState, useCallback, useMemo, useRef } from 'react';

/**
 * Hook for managing async data loading state
 */
export function useAsyncData(initialState = null) {
  const [data, setData] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (asyncFunction) => {
    try {
      setLoading(true);
      setError(null);
      const result = await asyncFunction();
      setData(result);
      return result;
    } catch (err) {
      console.error('Async operation failed:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(initialState);
    setError(null);
    setLoading(false);
  }, [initialState]);

  return { data, loading, error, execute, reset };
}

/**
 * Hook for plot export functionality
 */
export function usePlotExport(plotRef) {
  const exportPlot = useCallback((format) => {
    if (!plotRef.current) return;

    const plotlyDiv = plotRef.current.el;

    if (format === 'png' || format === 'svg') {
      window.Plotly.downloadImage(plotlyDiv, {
        format: format,
        width: 1200,
        height: 800,
        filename: `nyx-plot-${Date.now()}`,
      });
    } else if (format === 'json') {
      const data = plotRef.current.props.data;
      const dataStr = JSON.stringify(data, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `nyx-data-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
  }, [plotRef]);

  const resetView = useCallback(() => {
    if (plotRef.current?.el) {
      window.Plotly.relayout(plotRef.current.el, {
        'xaxis.autorange': true,
        'yaxis.autorange': true,
      });
    }
  }, [plotRef]);

  return { exportPlot, resetView };
}

/**
 * Hook for debouncing values
 */
export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useMemo(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook for managing previous value
 */
export function usePrevious(value) {
  const ref = useRef();

  useMemo(() => {
    ref.current = value;
  });

  return ref.current;
}

/**
 * Hook for window size
 */
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useMemo(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}
