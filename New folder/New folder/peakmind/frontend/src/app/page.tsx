'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useUser } from '@clerk/nextjs';
import { Brain, Activity, CheckCircle, Flame, Plus, Trash2, Loader2, Zap, X } from 'lucide-react';
import { fetchTasks, createTask, updateTask, deleteTask, fetchEnergyLogs, logEnergy, Task, EnergyLog } from '@/lib/api';

// ── Helpers ────────────────────────────────────────────────────────────────
const PRIORITY_LABELS: Record<number, { label: string; color: string }> = {
  1: { label: 'Low',    color: 'text-slate-400 bg-slate-700' },
  2: { label: 'Medium', color: 'text-yellow-400 bg-yellow-900/40' },
  3: { label: 'High',   color: 'text-red-400 bg-red-900/40' },
};

// ── Main Dashboard ─────────────────────────────────────────────────────────
export default function Home() {
  const { user, isLoaded } = useUser();
  const userId = user?.id ?? '';

  // Tasks state
  const [tasks, setTasks]           = useState<Task[]>([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState(2);
  const [addingTask, setAddingTask] = useState(false);
  const [showTaskForm, setShowTaskForm] = useState(false);

  // Energy state
  const [energyLogs, setEnergyLogs]     = useState<EnergyLog[]>([]);
  const [energyLoading, setEnergyLoading] = useState(true);
  const [energyScore, setEnergyScore]   = useState(70);
  const [energyMood, setEnergyMood]     = useState('');
  const [sleepHours, setSleepHours]     = useState(7);
  const [loggingEnergy, setLoggingEnergy] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState<string | null>(null);
  const [showEnergyForm, setShowEnergyForm] = useState(false);

  // Load tasks
  const loadTasks = useCallback(async () => {
    if (!userId) return;
    try {
      setTasksLoading(true);
      const data = await fetchTasks(userId);
      setTasks(data);
    } catch (e) {
      console.error(e);
    } finally {
      setTasksLoading(false);
    }
  }, [userId]);

  // Load energy logs
  const loadEnergy = useCallback(async () => {
    if (!userId) return;
    try {
      setEnergyLoading(true);
      const data = await fetchEnergyLogs(userId);
      setEnergyLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setEnergyLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (isLoaded && userId) {
      loadTasks();
      loadEnergy();
    }
  }, [isLoaded, userId, loadTasks, loadEnergy]);

  // Handlers
  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim() || !userId) return;
    setAddingTask(true);
    try {
      await createTask({ user_id: userId, title: newTaskTitle.trim(), priority: newTaskPriority, is_completed: false });
      setNewTaskTitle('');
      setNewTaskPriority(2);
      setShowTaskForm(false);
      await loadTasks();
    } catch (e) { console.error(e); }
    finally { setAddingTask(false); }
  };

  const handleToggleTask = async (task: Task) => {
    if (!task.id) return;
    try {
      await updateTask(task.id, { ...task, is_completed: !task.is_completed });
      await loadTasks();
    } catch (e) { console.error(e); }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId);
      await loadTasks();
    } catch (e) { console.error(e); }
  };

  const handleLogEnergy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId) return;
    setLoggingEnergy(true);
    try {
      const result = await logEnergy({ user_id: userId, score: energyScore, mood: energyMood || undefined, sleep_hours: sleepHours });
      setAiSuggestion(result.ai_suggestion);
      setShowEnergyForm(false);
      await loadEnergy();
    } catch (e) { console.error(e); }
    finally { setLoggingEnergy(false); }
  };

  // Derived
  const latestEnergy = energyLogs[0];
  const pendingTasks = tasks.filter(t => !t.is_completed);
  const completedTasks = tasks.filter(t => t.is_completed);

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-brand-400" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 text-center p-8">
        <Brain className="w-16 h-16 text-brand-400" />
        <h1 className="text-3xl font-bold text-slate-100">Welcome to PeakMind AI</h1>
        <p className="text-slate-400 max-w-md">Sign in to access your personal AI performance coach, track tasks, log energy, and get AI-powered insights.</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen p-6 lg:p-10 max-w-7xl mx-auto space-y-10">

      {/* ── Hero ── */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-4xl lg:text-5xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-brand-500 to-purple-400">
            Welcome back, {user.firstName ?? 'Creator'}.
          </h1>
          <p className="mt-2 text-slate-400 text-lg">PeakMind AI is ready to boost your performance today.</p>
        </div>
        <div className="flex items-center gap-4 glass-panel px-6 py-3">
          <div className="flex items-center gap-2">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="font-semibold text-slate-200">{completedTasks.length} Done Today</span>
          </div>
          <div className="w-px h-6 bg-slate-700" />
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            <span className="font-semibold text-slate-200">
              Energy: {latestEnergy ? `${latestEnergy.score}%` : 'Not logged'}
            </span>
          </div>
        </div>
      </header>

      {/* ── AI Suggestion Banner ── */}
      {aiSuggestion && (
        <section className="glass-panel p-5 bg-gradient-to-br from-brand-900/40 to-slate-900 border-brand-500/30 flex items-start gap-4">
          <div className="p-2 bg-brand-500 rounded-lg shrink-0">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold text-brand-300 mb-1">AI Coach Insight</p>
            <p className="text-slate-200">{aiSuggestion}</p>
          </div>
          <button onClick={() => setAiSuggestion(null)} className="text-slate-500 hover:text-slate-300 transition-colors">
            <X className="w-4 h-4" />
          </button>
        </section>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* ── Tasks Panel ── */}
        <section className="lg:col-span-2 glass-panel p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-brand-500/20 rounded-lg text-brand-400">
                <CheckCircle className="w-5 h-5" />
              </div>
              <h2 className="text-xl font-semibold text-slate-100">Smart Tasks</h2>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-400">{pendingTasks.length} pending</span>
              <button
                onClick={() => setShowTaskForm(v => !v)}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-sm font-medium transition-colors"
              >
                <Plus className="w-4 h-4" /> Add Task
              </button>
            </div>
          </div>

          {/* Add Task Form */}
          {showTaskForm && (
            <form onSubmit={handleAddTask} className="flex flex-col gap-3 p-4 bg-slate-800/60 rounded-xl border border-slate-700">
              <input
                value={newTaskTitle}
                onChange={e => setNewTaskTitle(e.target.value)}
                placeholder="Task title..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500 transition-colors"
                required
              />
              <div className="flex gap-3">
                <select
                  value={newTaskPriority}
                  onChange={e => setNewTaskPriority(Number(e.target.value))}
                  className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
                >
                  <option value={1}>Low Priority</option>
                  <option value={2}>Medium Priority</option>
                  <option value={3}>High Priority</option>
                </select>
                <button
                  type="submit"
                  disabled={addingTask}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
                >
                  {addingTask ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Save Task'}
                </button>
              </div>
            </form>
          )}

          {/* Task List */}
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
            {tasksLoading ? (
              <div className="flex justify-center py-8">
                <Loader2 className="w-6 h-6 animate-spin text-brand-400" />
              </div>
            ) : tasks.length === 0 ? (
              <p className="text-slate-500 text-center py-8">No tasks yet. Add your first task!</p>
            ) : (
              tasks.map(task => {
                const pri = PRIORITY_LABELS[task.priority] ?? PRIORITY_LABELS[1];
                return (
                  <div
                    key={task.id}
                    className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                      task.is_completed
                        ? 'border-slate-800 bg-slate-900/40 opacity-60'
                        : 'border-slate-700 bg-slate-800/50 hover:border-slate-600'
                    }`}
                  >
                    <button
                      onClick={() => handleToggleTask(task)}
                      className={`w-5 h-5 rounded shrink-0 border-2 flex items-center justify-center transition-colors ${
                        task.is_completed ? 'bg-brand-500 border-brand-500' : 'border-brand-500 hover:bg-brand-500/20'
                      }`}
                    >
                      {task.is_completed && <CheckCircle className="w-3 h-3 text-white" />}
                    </button>
                    <span className={`flex-1 text-sm ${task.is_completed ? 'line-through text-slate-500' : 'text-slate-200'}`}>
                      {task.title}
                    </span>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${pri.color}`}>{pri.label}</span>
                    <button
                      onClick={() => task.id && handleDeleteTask(task.id)}
                      className="text-slate-600 hover:text-red-400 transition-colors ml-1"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </section>

        {/* ── Energy Panel ── */}
        <section className="glass-panel p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-emerald-500/20 rounded-lg text-emerald-400">
                <Zap className="w-5 h-5" />
              </div>
              <h2 className="text-xl font-semibold text-slate-100">Energy</h2>
            </div>
            <button
              onClick={() => setShowEnergyForm(v => !v)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors"
            >
              <Plus className="w-4 h-4" /> Log
            </button>
          </div>

          {/* Current energy */}
          {latestEnergy ? (
            <div className="text-center py-4">
              <div className="relative inline-flex items-center justify-center w-28 h-28">
                <svg className="w-28 h-28 -rotate-90" viewBox="0 0 36 36">
                  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#1e293b" strokeWidth="3" />
                  <circle
                    cx="18" cy="18" r="15.9" fill="none"
                    stroke={latestEnergy.score >= 70 ? '#10b981' : latestEnergy.score >= 40 ? '#f59e0b' : '#ef4444'}
                    strokeWidth="3"
                    strokeDasharray={`${latestEnergy.score} 100`}
                    strokeLinecap="round"
                  />
                </svg>
                <span className="absolute text-2xl font-bold text-slate-100">{latestEnergy.score}%</span>
              </div>
              {latestEnergy.mood && <p className="text-slate-400 text-sm mt-2">Mood: {latestEnergy.mood}</p>}
              {latestEnergy.sleep_hours && <p className="text-slate-500 text-xs">Sleep: {latestEnergy.sleep_hours}h</p>}
            </div>
          ) : !energyLoading ? (
            <p className="text-slate-500 text-center py-4 text-sm">No energy logged yet.</p>
          ) : (
            <div className="flex justify-center py-4">
              <Loader2 className="w-6 h-6 animate-spin text-emerald-400" />
            </div>
          )}

          {/* Log Energy Form */}
          {showEnergyForm && (
            <form onSubmit={handleLogEnergy} className="flex flex-col gap-3 p-4 bg-slate-800/60 rounded-xl border border-slate-700">
              <label className="text-xs text-slate-400 font-medium">Energy Score: <span className="text-emerald-400 font-bold">{energyScore}%</span></label>
              <input
                type="range" min={0} max={100} value={energyScore}
                onChange={e => setEnergyScore(Number(e.target.value))}
                className="w-full accent-emerald-500"
              />
              <input
                value={energyMood}
                onChange={e => setEnergyMood(e.target.value)}
                placeholder="Mood (e.g. focused, tired...)"
                className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 placeholder-slate-500 text-sm focus:outline-none focus:border-emerald-500"
              />
              <div className="flex items-center gap-2">
                <label className="text-xs text-slate-400 shrink-0">Sleep (hrs):</label>
                <input
                  type="number" min={0} max={24} step={0.5} value={sleepHours}
                  onChange={e => setSleepHours(Number(e.target.value))}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 text-sm focus:outline-none focus:border-emerald-500"
                />
              </div>
              <button
                type="submit"
                disabled={loggingEnergy}
                className="flex items-center justify-center gap-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-600 disabled:opacity-50 text-white rounded-lg font-medium text-sm transition-colors"
              >
                {loggingEnergy ? <Loader2 className="w-4 h-4 animate-spin" /> : '🤖 Log & Get AI Tip'}
              </button>
            </form>
          )}

          {/* Recent logs */}
          {energyLogs.length > 1 && (
            <div className="space-y-2 mt-2">
              <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">Recent</p>
              {energyLogs.slice(1, 4).map(log => (
                <div key={log.id} className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">{log.mood ?? 'No mood'}</span>
                  <span className={`font-semibold ${log.score >= 70 ? 'text-emerald-400' : log.score >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {log.score}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>

      {/* ── Stats Bar ── */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Tasks',     value: tasks.length,          color: 'text-brand-400' },
          { label: 'Completed',       value: completedTasks.length, color: 'text-emerald-400' },
          { label: 'Pending',         value: pendingTasks.length,   color: 'text-yellow-400' },
          { label: 'Energy Logs',     value: energyLogs.length,     color: 'text-purple-400' },
        ].map(stat => (
          <div key={stat.label} className="glass-panel p-4 text-center">
            <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
            <p className="text-slate-400 text-sm mt-1">{stat.label}</p>
          </div>
        ))}
      </section>

    </main>
  );
}
