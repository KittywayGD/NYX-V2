import { useState } from 'react';
import { MessageSquare, Box, Settings, HelpCircle } from 'lucide-react';
import useNyxStore from '../store/nyxStore';
import SettingsPanel from './SettingsPanel';

function Sidebar() {
  const { clearMessages, modules } = useNyxStore();
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="w-16 bg-nyx-darker border-r border-gray-700 flex flex-col items-center py-4 space-y-4">
      {/* Logo */}
      <div className="w-10 h-10 bg-nyx-accent rounded-lg flex items-center justify-center font-bold text-lg">
        N
      </div>

      <div className="h-px w-10 bg-gray-700"></div>

      {/* Navigation */}
      <nav className="flex-1 flex flex-col items-center space-y-4">
        <SidebarButton icon={<MessageSquare />} tooltip="Chat" active />
        <SidebarButton icon={<Box />} tooltip="Sandboxes" />
        <SidebarButton
          icon={<Settings />}
          tooltip="Paramètres"
          onClick={() => setShowSettings(true)}
        />
      </nav>

      <div className="h-px w-10 bg-gray-700"></div>

      {/* Bottom */}
      <SidebarButton icon={<HelpCircle />} tooltip="Aide" />

      {/* Module count indicator */}
      <div className="text-xs text-gray-500">
        {modules.length}
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
        w-10 h-10 rounded-lg flex items-center justify-center
        transition-colors relative group
        ${active
          ? 'bg-nyx-accent text-white'
          : 'text-gray-400 hover:bg-gray-700 hover:text-white'
        }
      `}
      title={tooltip}
    >
      {icon}

      {/* Tooltip */}
      <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
        {tooltip}
      </div>
    </button>
  );
}

export default Sidebar;
