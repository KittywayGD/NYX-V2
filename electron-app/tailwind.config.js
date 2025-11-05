/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nyx-dark': '#0f172a',
        'nyx-darker': '#020617',
        'nyx-accent': '#3b82f6',
        'nyx-accent-hover': '#2563eb',
        'nyx-success': '#10b981',
        'nyx-warning': '#f59e0b',
        'nyx-error': '#ef4444',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}
