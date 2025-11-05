import { useEffect, useRef, useState } from 'react';
import Matter from 'matter-js';
import Plot from 'react-plotly.js';
import { Play, Pause, RotateCcw, Download, Settings } from 'lucide-react';

function PhysicsSandbox({ data }) {
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [simType, setSimType] = useState(null);

  useEffect(() => {
    loadSimulation();
  }, [data]);

  const loadSimulation = async () => {
    try {
      setLoading(true);
      const query = data?.original_query || '';
      const queryLower = query.toLowerCase();

      let type = 'projectile';
      if (queryLower.includes('pendule') || queryLower.includes('pendulum')) {
        type = 'pendulum';
      } else if (queryLower.includes('collision')) {
        type = 'collision';
      } else if (queryLower.includes('onde') || queryLower.includes('wave')) {
        type = 'wave';
      }

      setSimType(type);

      // Get simulation parameters
      const params = {
        initial_velocity: 20,
        angle_degrees: 45,
        height: 0,
        mass: 1.0,
        duration: 10,
      };

      const result = await window.nyxAPI.physicsSimulate({
        simulation_type: type,
        parameters: params,
      });

      if (result.success) {
        setSimulationData(result);
      }
    } catch (err) {
      console.error('Error loading simulation:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-gray-400">Chargement de la simulation...</div>;
  }

  if (!simulationData) {
    return <div className="text-gray-400">Aucune donnée de simulation</div>;
  }

  return (
    <div className="space-y-4">
      {simType === 'projectile' && <ProjectileSimulation data={simulationData} />}
      {simType === 'pendulum' && <PendulumSimulation data={simulationData} />}
      {simType === 'collision' && <CollisionSimulation data={simulationData} />}
      {simType === 'wave' && <WaveSimulation data={simulationData} />}
    </div>
  );
}

// Projectile Simulation with Matter.js
function ProjectileSimulation({ data }) {
  const canvasRef = useRef(null);
  const engineRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Create Matter.js engine
    const Engine = Matter.Engine;
    const Render = Matter.Render;
    const World = Matter.World;
    const Bodies = Matter.Bodies;

    const engine = Engine.create();
    engineRef.current = engine;

    const render = Render.create({
      element: canvasRef.current,
      engine: engine,
      options: {
        width: canvasRef.current.offsetWidth,
        height: 400,
        wireframes: false,
        background: '#0f172a',
      },
    });

    // Create ground
    const ground = Bodies.rectangle(400, 390, 810, 20, {
      isStatic: true,
      render: { fillStyle: '#475569' },
    });

    // Create projectile
    const projectile = Bodies.circle(50, 350, 10, {
      restitution: 0.8,
      render: { fillStyle: '#3b82f6' },
    });

    // Apply initial velocity
    const angle = (data.parameters.angle / 180) * Math.PI;
    const v0 = data.parameters.initial_velocity * 10; // Scale for visualization
    Matter.Body.setVelocity(projectile, {
      x: v0 * Math.cos(angle),
      y: -v0 * Math.sin(angle),
    });

    World.add(engine.world, [ground, projectile]);

    Render.run(render);

    return () => {
      Render.stop(render);
      World.clear(engine.world);
      Engine.clear(engine);
      render.canvas.remove();
    };
  }, [data]);

  useEffect(() => {
    if (!engineRef.current) return;

    const Engine = Matter.Engine;
    const Runner = Matter.Runner;

    if (isPlaying) {
      const runner = Runner.create();
      Runner.run(runner, engineRef.current);
      return () => Runner.stop(runner);
    }
  }, [isPlaying]);

  const exportData = () => {
    const dataStr = JSON.stringify(data, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `projectile-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      {/* Canvas */}
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold">Simulation Projectile</h4>
          <div className="flex gap-2">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-2 hover:bg-gray-700 rounded transition-colors"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <button
              onClick={exportData}
              className="p-2 hover:bg-gray-700 rounded transition-colors"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div ref={canvasRef} className="bg-nyx-darker rounded" />
      </div>

      {/* Trajectory Plot */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Trajectoire</h4>
          <Plot
            data={[{
              x: data.data.x,
              y: data.data.y,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#3b82f6', width: 2 },
              name: 'Trajectoire',
            }]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Distance (m)', gridcolor: '#334155' },
              yaxis: { title: 'Hauteur (m)', gridcolor: '#334155' },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Energy Plot */}
      {data.data?.energy && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Énergie</h4>
          <Plot
            data={[
              {
                x: data.data.time,
                y: data.data.energy.map(e => e.kinetic),
                type: 'scatter',
                mode: 'lines',
                name: 'Cinétique',
                line: { color: '#3b82f6' },
              },
              {
                x: data.data.time,
                y: data.data.energy.map(e => e.potential),
                type: 'scatter',
                mode: 'lines',
                name: 'Potentielle',
                line: { color: '#10b981' },
              },
              {
                x: data.data.time,
                y: data.data.energy.map(e => e.total),
                type: 'scatter',
                mode: 'lines',
                name: 'Totale',
                line: { color: '#f59e0b', dash: 'dash' },
              },
            ]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Énergie (J)', gridcolor: '#334155' },
              legend: { x: 1, xanchor: 'right', y: 1 },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}

      {/* Analysis */}
      {data.analysis && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Analyse</h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Hauteur max</div>
              <div className="text-lg font-semibold">{data.analysis.max_height?.toFixed(2)} m</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Portée</div>
              <div className="text-lg font-semibold">{data.analysis.range?.toFixed(2)} m</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Temps de vol</div>
              <div className="text-lg font-semibold">{data.analysis.flight_time?.toFixed(2)} s</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Temps hauteur max</div>
              <div className="text-lg font-semibold">{data.analysis.max_height_time?.toFixed(2)} s</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Pendulum Simulation
function PendulumSimulation({ data }) {
  const canvasRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!canvasRef.current) return;

    const Engine = Matter.Engine;
    const Render = Matter.Render;
    const World = Matter.World;
    const Bodies = Matter.Bodies;
    const Constraint = Matter.Constraint;

    const engine = Engine.create();
    engine.world.gravity.y = 1;

    const render = Render.create({
      element: canvasRef.current,
      engine: engine,
      options: {
        width: canvasRef.current.offsetWidth,
        height: 400,
        wireframes: false,
        background: '#0f172a',
      },
    });

    // Anchor point
    const anchor = { x: 400, y: 50 };

    // Pendulum bob
    const length = data.parameters.length * 100; // Scale
    const angle = (data.parameters.initial_angle / 180) * Math.PI;
    const bob = Bodies.circle(
      anchor.x + length * Math.sin(angle),
      anchor.y + length * Math.cos(angle),
      20,
      {
        density: 0.04,
        render: { fillStyle: '#3b82f6' },
      }
    );

    // String constraint
    const string = Constraint.create({
      pointA: anchor,
      bodyB: bob,
      length: length,
      stiffness: 1,
      render: { strokeStyle: '#475569', lineWidth: 2 },
    });

    World.add(engine.world, [bob, string]);
    Render.run(render);

    if (isPlaying) {
      const Runner = Matter.Runner;
      const runner = Runner.create();
      Runner.run(runner, engine);
    }

    return () => {
      Render.stop(render);
      World.clear(engine.world);
      Engine.clear(engine);
      render.canvas.remove();
    };
  }, [data, isPlaying]);

  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold">Simulation Pendule</h4>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>
        </div>
        <div ref={canvasRef} className="bg-nyx-darker rounded" />
      </div>

      {/* Angle vs Time */}
      {data.data && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Angle vs Temps</h4>
          <Plot
            data={[{
              x: data.data.time,
              y: data.data.angle,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#3b82f6', width: 2 },
            }]}
            layout={{
              paper_bgcolor: '#1e293b',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              xaxis: { title: 'Temps (s)', gridcolor: '#334155' },
              yaxis: { title: 'Angle (°)', gridcolor: '#334155' },
              margin: { l: 50, r: 30, t: 30, b: 50 },
            }}
            config={{ responsive: true, displaylogo: false }}
            style={{ width: '100%', height: '300px' }}
          />
        </div>
      )}
    </div>
  );
}

// Collision Simulation
function CollisionSimulation({ data }) {
  const canvasRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!canvasRef.current || !data.data?.frames) return;

    const Engine = Matter.Engine;
    const Render = Matter.Render;
    const World = Matter.World;
    const Bodies = Matter.Bodies;
    const Runner = Matter.Runner;

    const engine = Engine.create();
    const render = Render.create({
      element: canvasRef.current,
      engine: engine,
      options: {
        width: canvasRef.current.offsetWidth,
        height: 400,
        wireframes: false,
        background: '#0f172a',
      },
    });

    // Ground and walls
    const ground = Bodies.rectangle(400, 390, 810, 20, {
      isStatic: true,
      render: { fillStyle: '#475569' },
    });
    const leftWall = Bodies.rectangle(5, 200, 10, 400, { isStatic: true });
    const rightWall = Bodies.rectangle(795, 200, 10, 400, { isStatic: true });

    // Create balls from first frame
    const firstFrame = data.data.frames[0];
    const balls = firstFrame.objects.map(obj =>
      Bodies.circle(obj.x * 80, 200 - obj.y * 40, obj.radius * 80, {
        restitution: 0.9,
        render: { fillStyle: '#3b82f6' },
      })
    );

    World.add(engine.world, [ground, leftWall, rightWall, ...balls]);
    Render.run(render);

    if (isPlaying) {
      const runner = Runner.create();
      Runner.run(runner, engine);
    }

    return () => {
      Render.stop(render);
      World.clear(engine.world);
      Engine.clear(engine);
      render.canvas.remove();
    };
  }, [data, isPlaying]);

  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold">Simulation Collision</h4>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>
        </div>
        <div ref={canvasRef} className="bg-nyx-darker rounded" />
      </div>
    </div>
  );
}

// Wave Simulation
function WaveSimulation({ data }) {
  const [frameIndex, setFrameIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!isPlaying || !data.data?.frames) return;

    const interval = setInterval(() => {
      setFrameIndex(prev => (prev + 1) % data.data.frames.length);
    }, 50);

    return () => clearInterval(interval);
  }, [isPlaying, data.data?.frames]);

  if (!data.data?.frames) return null;

  const currentFrame = data.data.frames[frameIndex];

  return (
    <div className="space-y-4">
      <div className="glass p-4 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold">Propagation d'Onde</h4>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>
        </div>
        <Plot
          data={[{
            x: currentFrame.x,
            y: currentFrame.y,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#3b82f6', width: 3 },
          }]}
          layout={{
            paper_bgcolor: '#1e293b',
            plot_bgcolor: '#0f172a',
            font: { color: '#e2e8f0' },
            xaxis: { title: 'Position', gridcolor: '#334155', range: [0, 10] },
            yaxis: { title: 'Amplitude', gridcolor: '#334155', range: [-2, 2] },
            margin: { l: 50, r: 30, t: 30, b: 50 },
          }}
          config={{ responsive: true, displaylogo: false }}
          style={{ width: '100%', height: '300px' }}
        />
        <div className="mt-3 flex items-center gap-3">
          <input
            type="range"
            min="0"
            max={data.data.frames.length - 1}
            value={frameIndex}
            onChange={(e) => setFrameIndex(parseInt(e.target.value))}
            className="flex-1"
          />
          <span className="text-sm text-gray-400">
            t = {currentFrame.time.toFixed(2)} s
          </span>
        </div>
      </div>

      {/* Parameters */}
      {data.parameters && (
        <div className="glass p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Paramètres</h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Type</div>
              <div className="font-semibold">{data.parameters.wave_type}</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Fréquence</div>
              <div className="font-semibold">{data.parameters.frequency} Hz</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Amplitude</div>
              <div className="font-semibold">{data.parameters.amplitude}</div>
            </div>
            <div className="p-2 bg-nyx-dark rounded">
              <div className="text-gray-400">Vitesse</div>
              <div className="font-semibold">{data.parameters.speed} m/s</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default PhysicsSandbox;
