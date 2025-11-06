import { useState } from 'react';
import { MessageSquare, Box, Settings, HelpCircle, Cpu } from 'lucide-react';
import useNyxStore from '../store/nyxStore';
import SettingsPanel from './SettingsPanel';

function Sidebar() {
  const { clearMessages, modules } = useNyxStore();
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="w-20 cyber-glass border-r border-cyber-cyan border-opacity-20 flex flex-col items-center py-6 space-y-6">
      {/* Logo - Cyberpunk */}
      <div className="w-14 h-14 bg-gradient-to-br from-cyber-cyan to-cyber-purple rounded-lg flex items-center justify-center font-display font-black text-2xl relative group cursor-pointer neon-border shadow-neon-cyan">
        <span className="holographic">N</span>
        <div className="absolute inset-0 bg-cyber-cyan rounded-lg blur-xl opacity-0 group-hover:opacity-30 transition-opacity"></div>
      </div>

      <div className="h-px w-12 bg-gradient-to-r from-transparent via-cyber-cyan to-transparent opacity-30"></div>

      {/* Navigation */}
      <nav className="flex-1 flex flex-col items-center space-y-4">
        <SidebarButton icon={<MessageSquare />} tooltip="CHAT" active />
        <SidebarButton icon={<Box />} tooltip="SANDBOXES" />
        <SidebarButton
          icon={<Settings />}
          tooltip="PARAMÈTRES"
          onClick={() => setShowSettings(true)}
        />
      </nav>

      <div className="h-px w-12 bg-gradient-to-r from-transparent via-cyber-cyan to-transparent opacity-30"></div>

      {/* Bottom */}
      <SidebarButton icon={<HelpCircle />} tooltip="AIDE" />

      {/* Module count indicator - Cyberpunk */}
      <div className="flex flex-col items-center gap-1">
        <Cpu className="w-5 h-5 text-cyber-cyan animate-pulse" />
        <div className="text-xs font-display font-bold text-cyber-cyan">
          {modules.length}
        </div>
      </div>

      {/* Settings Panel Modal */}
      {showSettings && <SettingsPanel onClose={() => setShowSettings(false)} />}
    </div>
  );
}

function SidebarButton({ icon, tooltip, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`
        w-12 h-12 rounded-lg flex items-center justify-center
        transition-all duration-300 relative group font-display
        ${active
          ? 'bg-cyber-cyan bg-opacity-20 text-cyber-cyan shadow-neon-cyan border border-cyber-cyan'
          : 'text-cyber-cyan text-opacity-50 hover:bg-cyber-cyan hover:bg-opacity-10 hover:text-cyber-cyan border border-transparent hover:border-cyber-cyan hover:border-opacity-30'
        }
      `}
      title={tooltip}
    >
      {icon}

      {/* Glow effect on hover */}
      <div className="absolute inset-0 bg-cyber-cyan rounded-lg blur-lg opacity-0 group-hover:opacity-20 transition-opacity"></div>

      {/* Tooltip - Cyberpunk */}
      <div className="absolute left-full ml-3 px-3 py-2 cyber-glass border border-cyber-cyan border-opacity-30 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50 font-display uppercase tracking-wider text-cyber-cyan shadow-neon-cyan">
        <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-1 w-2 h-2 bg-cyber-cyan rotate-45 border-l border-b border-cyber-cyan border-opacity-30"></div>
        {tooltip}
      </div>
    </button>
  );
}

export default Sidebar;
