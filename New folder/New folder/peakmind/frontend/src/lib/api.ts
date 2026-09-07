const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ── Shared fetch helper ────────────────────────────────────────────────────

async function apiFetch(path: string, token: string, options: RequestInit = {}): Promise<Response> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...(options.headers ?? {}),
    },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => res.statusText);
    throw new Error(body || `HTTP ${res.status}`);
  }
  return res;
}

// ── Types ──────────────────────────────────────────────────────────────────

export interface Task {
  id?: number;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  priority: number;
  estimated_time_minutes?: number;
  created_at?: string;
}

export interface EnergyLog {
  id?: number;
  user_id: string;
  score: number;
  mood?: string;
  sleep_hours?: number;
  logged_at?: string;
}

export interface StudyPlan {
  id?: number;
  user_id: string;
  topic: string;
  target_date?: string;
  duration_minutes?: number;
  is_completed: boolean;
  created_at?: string;
}

export interface FitnessLog {
  id?: number;
  user_id: string;
  exercise_type: string;
  duration_minutes: number;
  calories_burned?: number;
  notes?: string;
  is_completed: boolean;
  logged_at?: string;
}

// ── Tasks ──────────────────────────────────────────────────────────────────

export async function fetchTasks(userId: string, token: string): Promise<Task[]> {
  const res = await apiFetch(`/api/tasks/?user_id=${encodeURIComponent(userId)}`, token);
  return res.json();
}

export async function createTask(task: Omit<Task, 'id' | 'created_at'>, token: string): Promise<Task> {
  const res = await apiFetch('/api/tasks/', token, {
    method: 'POST',
    body: JSON.stringify(task),
  });
  return res.json();
}

export async function updateTask(taskId: number, task: Partial<Task>, token: string): Promise<Task> {
  const res = await apiFetch(`/api/tasks/${taskId}`, token, {
    method: 'PUT',
    body: JSON.stringify(task),
  });
  return res.json();
}

export async function deleteTask(taskId: number, token: string): Promise<void> {
  await apiFetch(`/api/tasks/${taskId}`, token, { method: 'DELETE' });
}

// ── Energy ─────────────────────────────────────────────────────────────────

export async function fetchEnergyLogs(userId: string, token: string): Promise<EnergyLog[]> {
  const res = await apiFetch(`/api/energy/?user_id=${encodeURIComponent(userId)}`, token);
  return res.json();
}

export async function logEnergy(
  log: Omit<EnergyLog, 'id' | 'logged_at'>,
  token: string
): Promise<{ log: EnergyLog; ai_suggestion: string }> {
  const res = await apiFetch('/api/energy/', token, {
    method: 'POST',
    body: JSON.stringify(log),
  });
  return res.json();
}

// ── Study Planner ───────────────────────────────────────────────────────────

export async function fetchStudyPlans(userId: string, token: string): Promise<StudyPlan[]> {
  const res = await apiFetch(`/api/study/?user_id=${encodeURIComponent(userId)}`, token);
  return res.json();
}

export async function createStudyPlan(
  plan: Omit<StudyPlan, 'id' | 'created_at'>,
  token: string
): Promise<StudyPlan> {
  const res = await apiFetch('/api/study/', token, {
    method: 'POST',
    body: JSON.stringify(plan),
  });
  return res.json();
}

export async function updateStudyPlan(
  planId: number,
  plan: Partial<StudyPlan>,
  token: string
): Promise<StudyPlan> {
  const res = await apiFetch(`/api/study/${planId}`, token, {
    method: 'PUT',
    body: JSON.stringify(plan),
  });
  return res.json();
}

export async function deleteStudyPlan(planId: number, token: string): Promise<void> {
  await apiFetch(`/api/study/${planId}`, token, { method: 'DELETE' });
}

// ── Fitness Coach ───────────────────────────────────────────────────────────

export async function fetchFitnessLogs(userId: string, token: string): Promise<FitnessLog[]> {
  const res = await apiFetch(`/api/fitness/?user_id=${encodeURIComponent(userId)}`, token);
  return res.json();
}

export async function createFitnessLog(
  log: Omit<FitnessLog, 'id' | 'logged_at'>,
  token: string
): Promise<{ log: FitnessLog; ai_suggestion: string }> {
  const res = await apiFetch('/api/fitness/', token, {
    method: 'POST',
    body: JSON.stringify(log),
  });
  return res.json();
}

export async function deleteFitnessLog(logId: number, token: string): Promise<void> {
  await apiFetch(`/api/fitness/${logId}`, token, { method: 'DELETE' });
}
