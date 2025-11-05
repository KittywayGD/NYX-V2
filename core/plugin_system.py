"""
Plugin System for NYX-V2
Permet d'ajouter des modules custom sans modifier le code core
"""

import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
import logging
import json

from modules.base_module import BaseModule

logger = logging.getLogger(__name__)


class PluginMetadata:
    """Métadonnées d'un plugin"""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get('name', 'Unknown')
        self.version = data.get('version', '1.0.0')
        self.author = data.get('author', 'Unknown')
        self.description = data.get('description', '')
        self.entry_point = data.get('entry_point')
        self.dependencies = data.get('dependencies', [])
        self.capabilities = data.get('capabilities', [])
        self.enabled = data.get('enabled', True)


class PluginLoader:
    """Chargeur de plugins pour NYX-V2"""

    def __init__(self, plugins_dir: str = None):
        """
        Initialize the plugin loader

        Args:
            plugins_dir: Directory containing plugins (default: ./plugins)
        """
        if plugins_dir is None:
            plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')

        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)

        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_metadata: Dict[str, PluginMetadata] = {}

        logger.info(f"Plugin loader initialized with directory: {self.plugins_dir}")

    def discover_plugins(self) -> List[str]:
        """
        Découvre tous les plugins disponibles

        Returns:
            Liste des noms de plugins trouvés
        """
        plugins = []

        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory does not exist: {self.plugins_dir}")
            return plugins

        for item in self.plugins_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                manifest_path = item / 'plugin.json'
                if manifest_path.exists():
                    plugins.append(item.name)
                    logger.info(f"Discovered plugin: {item.name}")

        return plugins

    def load_plugin_metadata(self, plugin_name: str) -> Optional[PluginMetadata]:
        """
        Charge les métadonnées d'un plugin

        Args:
            plugin_name: Nom du plugin

        Returns:
            PluginMetadata ou None si erreur
        """
        manifest_path = self.plugins_dir / plugin_name / 'plugin.json'

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metadata = PluginMetadata(data)
                self.plugin_metadata[plugin_name] = metadata
                return metadata
        except Exception as e:
            logger.error(f"Error loading metadata for plugin {plugin_name}: {e}")
            return None

    def load_plugin(self, plugin_name: str) -> Optional[Type[BaseModule]]:
        """
        Charge un plugin

        Args:
            plugin_name: Nom du plugin à charger

        Returns:
            Classe du module ou None si erreur
        """
        try:
            # Load metadata
            metadata = self.load_plugin_metadata(plugin_name)
            if not metadata:
                logger.error(f"Failed to load metadata for plugin: {plugin_name}")
                return None

            if not metadata.enabled:
                logger.info(f"Plugin {plugin_name} is disabled")
                return None

            # Check dependencies
            if not self._check_dependencies(metadata.dependencies):
                logger.error(f"Missing dependencies for plugin: {plugin_name}")
                return None

            # Load the module
            plugin_path = self.plugins_dir / plugin_name
            entry_point = metadata.entry_point or 'main.py'
            module_file = plugin_path / entry_point

            if not module_file.exists():
                logger.error(f"Entry point not found: {module_file}")
                return None

            # Import the module
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}",
                module_file
            )

            if spec is None or spec.loader is None:
                logger.error(f"Failed to create module spec for: {plugin_name}")
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

            # Find the module class
            module_class = None
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and
                    issubclass(obj, BaseModule) and
                    obj is not BaseModule):
                    module_class = obj
                    break

            if module_class is None:
                logger.error(f"No BaseModule subclass found in plugin: {plugin_name}")
                return None

            self.loaded_plugins[plugin_name] = module_class
            logger.info(f"✓ Plugin loaded successfully: {plugin_name} v{metadata.version}")

            return module_class

        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}", exc_info=True)
            return None

    def load_all_plugins(self) -> Dict[str, Type[BaseModule]]:
        """
        Charge tous les plugins disponibles

        Returns:
            Dict des classes de modules chargées
        """
        plugins = self.discover_plugins()
        loaded = {}

        for plugin_name in plugins:
            module_class = self.load_plugin(plugin_name)
            if module_class:
                loaded[plugin_name] = module_class

        logger.info(f"Loaded {len(loaded)}/{len(plugins)} plugins")
        return loaded

    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Décharge un plugin

        Args:
            plugin_name: Nom du plugin

        Returns:
            True si succès
        """
        try:
            if plugin_name in self.loaded_plugins:
                del self.loaded_plugins[plugin_name]

                # Remove from sys.modules
                module_name = f"plugins.{plugin_name}"
                if module_name in sys.modules:
                    del sys.modules[module_name]

                logger.info(f"Plugin unloaded: {plugin_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False

    def reload_plugin(self, plugin_name: str) -> Optional[Type[BaseModule]]:
        """
        Recharge un plugin

        Args:
            plugin_name: Nom du plugin

        Returns:
            Classe du module rechargée
        """
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name)

    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """
        Vérifie que toutes les dépendances sont installées

        Args:
            dependencies: Liste des packages requis

        Returns:
            True si toutes les dépendances sont présentes
        """
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                logger.warning(f"Missing dependency: {dep}")
                return False
        return True

    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les informations d'un plugin

        Args:
            plugin_name: Nom du plugin

        Returns:
            Dict avec les infos du plugin
        """
        metadata = self.plugin_metadata.get(plugin_name)
        if not metadata:
            return None

        return {
            'name': metadata.name,
            'version': metadata.version,
            'author': metadata.author,
            'description': metadata.description,
            'capabilities': metadata.capabilities,
            'enabled': metadata.enabled,
            'loaded': plugin_name in self.loaded_plugins,
        }

    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        Liste tous les plugins avec leurs infos

        Returns:
            Liste des infos de plugins
        """
        plugins = self.discover_plugins()
        return [self.get_plugin_info(name) for name in plugins if self.get_plugin_info(name)]


def create_plugin_template(plugin_name: str, plugin_dir: str = None) -> bool:
    """
    Crée un template de plugin

    Args:
        plugin_name: Nom du plugin
        plugin_dir: Répertoire (optionnel)

    Returns:
        True si succès
    """
    try:
        if plugin_dir is None:
            plugin_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins', plugin_name)

        plugin_path = Path(plugin_dir)
        plugin_path.mkdir(parents=True, exist_ok=True)

        # Create plugin.json
        manifest = {
            "name": plugin_name,
            "version": "1.0.0",
            "author": "Your Name",
            "description": f"Description of {plugin_name} plugin",
            "entry_point": "main.py",
            "dependencies": [],
            "capabilities": ["custom_capability"],
            "enabled": True
        }

        with open(plugin_path / 'plugin.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        # Create main.py
        main_code = f'''"""
{plugin_name} Plugin for NYX-V2
"""

from modules.base_module import BaseModule
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class {plugin_name.title().replace('_', '')}Module(BaseModule):
    """Custom module: {plugin_name}"""

    def __init__(self):
        super().__init__("{plugin_name}", "1.0.0")
        self.capabilities = ["custom_capability"]
        self.metadata = {{
            "description": "Custom {plugin_name} module",
            "author": "Your Name",
        }}

    def initialize(self) -> bool:
        """Initialize the module"""
        logger.info(f"Initializing {{self.name}} module...")
        # Add your initialization code here
        logger.info(f"✓ {{self.name}} module initialized")
        return True

    def can_handle(self, query: str) -> float:
        """
        Check if this module can handle a query

        Args:
            query: User query

        Returns:
            Confidence score (0.0 to 1.0)
        """
        query_lower = query.lower()

        # Add your keywords here
        keywords = {{
            'your_keyword': 0.9,
            'another_keyword': 0.8,
        }}

        score = 0.0
        for keyword, weight in keywords.items():
            if keyword in query_lower:
                score = max(score, weight)

        return min(score, 1.0)

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a query

        Args:
            query: User query
            context: Optional context

        Returns:
            Result dictionary
        """
        logger.info(f"Executing query: {{query}}")

        try:
            # Add your processing logic here
            result = {{
                "message": f"Processed by {{self.name}}",
                "query": query,
            }}

            return {{
                "success": True,
                "result": result,
            }}

        except Exception as e:
            logger.error(f"Error executing query: {{e}}")
            return {{
                "success": False,
                "error": str(e),
            }}

    def validate_result(self, result: Any, original_query: str) -> Dict[str, Any]:
        """Validate a result"""
        return {{
            "is_valid": True,
            "confidence": 0.9,
            "errors": [],
        }}
'''

        with open(plugin_path / 'main.py', 'w', encoding='utf-8') as f:
            f.write(main_code)

        # Create __init__.py
        with open(plugin_path / '__init__.py', 'w', encoding='utf-8') as f:
            f.write(f'"""Plugin: {plugin_name}"""\n')

        # Create README.md
        readme = f'''# {plugin_name} Plugin

## Description
Description of your plugin.

## Capabilities
- Capability 1
- Capability 2

## Usage
```python
# Example usage
```

## Configuration
Add any configuration needed.

## Dependencies
List any Python packages required.
'''

        with open(plugin_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme)

        logger.info(f"✓ Plugin template created: {plugin_path}")
        return True

    except Exception as e:
        logger.error(f"Error creating plugin template: {e}")
        return False
