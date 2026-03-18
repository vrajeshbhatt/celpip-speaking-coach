/**
 * CELPIP Speaking Coach — Frontend Application
 * Handles task flow, audio recording, timer, and results display.
 */

// ============================================================
// State
// ============================================================
const state = {
  currentView: 'practice',
  tasks: [],
  currentTask: null,
  currentPrompt: null,
  isRecording: false,
  mediaRecorder: null,
  audioChunks: [],
  prepTimerInterval: null,
  recordTimerInterval: null,
  prepTimeLeft: 0,
  recordTimeLeft: 0,
  fullTestMode: false,
  fullTestTasks: [],
  fullTestIndex: 0,
  fullTestResults: []
};

// ============================================================
// Initialization
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {
  await checkHealth();
  await loadTasks();
});

async function checkHealth() {
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    const badge = document.getElementById('healthBadge');
    const text = document.getElementById('healthText');

    if (data.whisper_loaded) {
      text.textContent = `Ready — Whisper ${data.whisper_model}`;
      badge.classList.remove('error');
    } else {
      text.textContent = 'Whisper not loaded — limited mode';
      badge.classList.add('error');
    }
  } catch (e) {
    const badge = document.getElementById('healthBadge');
    const text = document.getElementById('healthText');
    text.textContent = 'Server offline';
    badge.classList.add('error');
  }
}

async function loadTasks() {
  try {
    const res = await fetch('/api/tasks');
    const data = await res.json();
    state.tasks = data.tasks;
    renderTaskGrid();
  } catch (e) {
    console.error('Failed to load tasks:', e);
  }
}

// ============================================================
// Navigation
// ============================================================
function switchView(view) {
  state.currentView = view;
  
  // Update tabs
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.view === view);
  });

  // Update views
  document.getElementById('practiceView').classList.toggle('hidden', view !== 'practice');
  document.getElementById('fulltestView').classList.toggle('hidden', view !== 'fulltest');
  document.getElementById('historyView').classList.toggle('hidden', view !== 'history');
  document.getElementById('progressView').classList.toggle('hidden', view !== 'progress');

  // Load data for history/progress
  if (view === 'history') loadHistory();
  if (view === 'progress') loadProgress();
}

// ============================================================
// Task Grid
// ============================================================
function renderTaskGrid() {
  const grid = document.getElementById('taskGrid');
  let html = state.tasks.map(task => `
    <div class="task-card ${task.is_practice ? 'practice-task' : ''}" onclick="selectTask(${task.number})">
      <div class="task-number">${task.number === 0 ? '🎯' : task.number}</div>
      <div class="task-name">${task.name}</div>
      <div class="task-desc">${task.description}</div>
      <div class="task-timing">
        ${task.is_practice ? '<span class="practice-badge">UNSCORED</span>' : ''}
        <span>⏱ ${task.prep_time}s prep</span>
        <span>🎤 ${task.response_time}s speak</span>
      </div>
    </div>
  `).join('');
  
  // Add 'Fetch New Tasks' card
  html += `
    <div class="task-card fetch-tasks-card" onclick="fetchNewTasks()">
      <div class="task-number">🔄</div>
      <div class="task-name">Fetch New Tasks</div>
      <div class="task-desc">Get fresh prompts and practice scenarios to keep your preparation challenging.</div>
      <div class="task-timing">
        <span style="color: var(--accent-primary); font-weight: 600;">+ Generate More</span>
      </div>
    </div>
  `;
  
  grid.innerHTML = html;
}

async function fetchNewTasks() {
  try {
    const btn = document.querySelector('.fetch-tasks-card');
    btn.innerHTML = '<div class="text-center" style="width: 100%;"><div class="spinner" style="margin-bottom:12px;"></div><div>Generating new prompts...</div></div>';
    
    const res = await fetch('/api/tasks/generate', { method: 'POST' });
    const data = await res.json();
    
    if (data.status === 'success') {
      alert(data.message);
      await loadTasks(); // Reload the task list
    }
  } catch (e) {
    console.error('Failed to fetch new tasks:', e);
    alert('Failed to fetch new tasks. Make sure the server is running.');
    renderTaskGrid(); // Reset loading state
  }
}

// ============================================================
// Task Flow
// ============================================================
async function selectTask(taskNumber) {
  try {
    const res = await fetch(`/api/tasks/${taskNumber}`);
    const data = await res.json();
    state.currentTask = data;
    state.currentPrompt = data.prompt;
    showPrepPhase();
  } catch (e) {
    console.error('Failed to load task:', e);
  }
}

function showPrepPhase() {
  const task = state.currentTask;
  
  document.getElementById('taskSelection').classList.add('hidden');
  document.getElementById('activeTask').classList.add('active');
  document.getElementById('prepPhase').classList.remove('hidden');
  document.getElementById('recordPhase').classList.add('hidden');
  document.getElementById('resultsPhase').classList.add('hidden');

  // Fill content
  document.getElementById('activeTaskName').textContent = `Task ${task.number}: ${task.name}`;
  document.getElementById('scenarioBox').textContent = task.prompt.scenario;
  
  const imageBox = document.getElementById('taskImageBox');
  const imageEl = document.getElementById('taskImage');
  if (task.prompt.image_url) {
    imageEl.src = task.prompt.image_url;
    imageBox.style.display = 'block';
  } else {
    imageBox.style.display = 'none';
    imageEl.src = '';
  }
  
  // Tips
  const tipsList = document.getElementById('tipsList');
  tipsList.innerHTML = task.tips.map(tip => `<li>${tip}</li>`).join('');

  // Start prep timer
  state.prepTimeLeft = task.prep_time;
  updatePrepTimer();
  const circumference = 2 * Math.PI * 78;
  document.getElementById('prepRingProgress').style.strokeDasharray = circumference;
  document.getElementById('prepRingProgress').style.strokeDashoffset = 0;

  state.prepTimerInterval = setInterval(() => {
    state.prepTimeLeft--;
    updatePrepTimer();
    
    // Update ring
    const progress = 1 - (state.prepTimeLeft / task.prep_time);
    const ring = document.getElementById('prepRingProgress');
    ring.style.strokeDashoffset = circumference * progress;
    
    // Color changes
    if (state.prepTimeLeft <= 5) {
      ring.classList.add('danger');
      ring.classList.remove('warning');
    } else if (state.prepTimeLeft <= 10) {
      ring.classList.add('warning');
    }

    if (state.prepTimeLeft <= 0) {
      clearInterval(state.prepTimerInterval);
      startRecording();
    }
  }, 1000);
}

function updatePrepTimer() {
  document.getElementById('prepSeconds').textContent = state.prepTimeLeft;
}

function startRecordingEarly() {
  clearInterval(state.prepTimerInterval);
  startRecording();
}

async function startRecording() {
  const task = state.currentTask;

  // Switch to recording phase
  document.getElementById('prepPhase').classList.add('hidden');
  document.getElementById('recordPhase').classList.remove('hidden');

  document.getElementById('recordTaskName').textContent = `Task ${task.number}: ${task.name}`;
  document.getElementById('recordScenarioBox').textContent = task.prompt.scenario;

  const recordImageBox = document.getElementById('recordTaskImageBox');
  const recordImageEl = document.getElementById('recordTaskImage');
  if (task.prompt.image_url) {
    recordImageEl.src = task.prompt.image_url;
    recordImageBox.style.display = 'block';
  } else {
    recordImageBox.style.display = 'none';
    recordImageEl.src = '';
  }

  // Start audio recording
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: { 
        channelCount: 1, 
        sampleRate: 16000,
        echoCancellation: true,
        noiseSuppression: true
      } 
    });
    
    state.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
    state.audioChunks = [];

    state.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) state.audioChunks.push(e.data);
    };

    state.mediaRecorder.onstop = () => {
      stream.getTracks().forEach(track => track.stop());
      analyzeRecording();
    };

    state.mediaRecorder.start(100); // Collect chunks every 100ms
    state.isRecording = true;
  } catch (e) {
    console.error('Microphone access denied:', e);
    alert('Microphone access is required. Please allow microphone access and try again.');
    cancelTask();
    return;
  }

  // Start recording timer
  state.recordTimeLeft = task.response_time;
  updateRecordTimer();
  const circumference = 2 * Math.PI * 78;
  const ring = document.getElementById('recordRingProgress');
  ring.style.strokeDasharray = circumference;
  ring.style.strokeDashoffset = 0;
  ring.classList.remove('warning', 'danger');

  state.recordTimerInterval = setInterval(() => {
    state.recordTimeLeft--;
    updateRecordTimer();

    const progress = 1 - (state.recordTimeLeft / task.response_time);
    ring.style.strokeDashoffset = circumference * progress;

    if (state.recordTimeLeft <= 10) {
      ring.classList.add('danger');
      ring.classList.remove('warning');
    } else if (state.recordTimeLeft <= 20) {
      ring.classList.add('warning');
    }

    if (state.recordTimeLeft <= 0) {
      stopRecording();
    }
  }, 1000);
}

function updateRecordTimer() {
  document.getElementById('recordSeconds').textContent = state.recordTimeLeft;
}

function stopRecordingEarly() {
  stopRecording();
}

function stopRecording() {
  clearInterval(state.recordTimerInterval);
  if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
    state.mediaRecorder.stop();
  }
  state.isRecording = false;
}

async function analyzeRecording() {
  // Show analyzing overlay
  document.getElementById('analyzingOverlay').classList.add('active');
  document.getElementById('analyzingText').textContent = 'Transcribing your speech...';

  try {
    // Create audio blob
    const audioBlob = new Blob(state.audioChunks, { type: 'audio/webm' });
    
    // Upload and analyze
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('task_type', state.fullTestMode ? 'full_test' : 'practice');
    formData.append('task_number', state.currentTask.number);
    formData.append('prompt', state.currentTask.prompt.scenario);

    document.getElementById('analyzingText').textContent = 'Analyzing pronunciation and prosody...';

    const res = await fetch('/api/audio/upload', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    document.getElementById('analyzingText').textContent = 'Generating scores and feedback...';
    await new Promise(r => setTimeout(r, 500)); // Brief pause for UX

    // Hide overlay
    document.getElementById('analyzingOverlay').classList.remove('active');

    // Show results
    if (state.fullTestMode) {
      state.fullTestResults.push(data);
      state.fullTestIndex++;
      if (state.fullTestIndex < state.fullTestTasks.length) {
        // Next task in full test
        state.currentTask = state.fullTestTasks[state.fullTestIndex];
        state.currentPrompt = state.currentTask.prompt;
        showPrepPhase();
      } else {
        // Full test complete — show summary
        showFullTestResults();
      }
    } else {
      showResults(data);
    }
  } catch (e) {
    console.error('Analysis error:', e);
    document.getElementById('analyzingOverlay').classList.remove('active');
    alert('Analysis failed. Please check that the server is running.');
  }
}

// ============================================================
// Results Display
// ============================================================
function showResults(data) {
  document.getElementById('prepPhase').classList.add('hidden');
  document.getElementById('recordPhase').classList.add('hidden');
  document.getElementById('resultsPhase').classList.remove('hidden');

  const scores = data.scores || {};
  const feedback = data.feedback || {};
  const overall = scores.overall || 0;
  const clb = scores.clb_level || 0;
  const levelLabel = scores.level_label || '';
  const isPractice = state.currentTask && state.currentTask.is_practice;

  let html = `
    <div class="score-dashboard">
      <div class="overall-score">
        <div class="score-circle ${overall >= 10 ? 'score-excellent' : overall >= 7 ? 'score-good' : overall >= 4 ? 'score-fair' : 'score-low'}">
          <div class="score-value">${isPractice ? '—' : overall.toFixed(1)}</div>
          <div class="score-label">${isPractice ? 'PRACTICE' : 'CELPIP'}</div>
        </div>
        ${isPractice ? '<div class="clb-badge" style="background: var(--bg-tertiary);">Unscored Warm-Up</div>' : `<div class="clb-badge">CLB ${clb} — ${levelLabel}</div>`}
        ${scores.level_descriptor ? `<p style="color: var(--text-secondary); margin-top: 8px; font-size: 0.9rem;">${scores.level_descriptor}</p>` : ''}
      </div>

      ${isPractice ? '' : `<div class="dimension-scores">
        ${renderDimensionCard('Content/Coherence', scores.content_coherence)}
        ${renderDimensionCard('Vocabulary', scores.vocabulary)}
        ${renderDimensionCard('Listenability', scores.listenability)}
        ${renderDimensionCard('Task Fulfillment', scores.task_fulfillment)}
      </div>`}

      ${isPractice ? '' : renderBenchmark(feedback.benchmark)}
      ${isPractice ? '' : renderPriorities(feedback.priorities)}
      ${isPractice ? '' : renderLevelAdvice(feedback.level_advice)}
      ${isPractice ? '' : renderFeedbackCards(feedback)}
      ${renderTranscript(data.transcript)}
      ${isPractice ? '' : renderModelAnswer(feedback.model_answer)}
    </div>

    <div class="btn-group" style="margin-top: 32px;">
      <button class="btn btn-secondary" onclick="cancelTask()">← Back to Tasks</button>
      <button class="btn btn-primary" onclick="retryTask()">Try Again</button>
    </div>
  `;

  document.getElementById('resultsContent').innerHTML = html;
}

function renderDimensionCard(name, score) {
  score = score || 0;
  const percent = (score / 12) * 100;
  let barClass = '';
  if (score >= 9) barClass = 'good';
  else if (score >= 6) barClass = 'warning';
  else barClass = 'danger';

  return `
    <div class="dimension-card">
      <div class="dimension-header">
        <span class="dimension-name">${name}</span>
        <span class="dimension-score">${score.toFixed(1)}</span>
      </div>
      <div class="score-bar-bg">
        <div class="score-bar-fill ${barClass}" style="width: ${percent}%"></div>
      </div>
    </div>
  `;
}

function renderBenchmark(benchmark) {
  if (!benchmark) return '';
  return `
    <div class="benchmark-box">
      <div class="target">Target: CLB ${benchmark.target_level}</div>
      <div class="message">${benchmark.message}</div>
    </div>
  `;
}

function renderPriorities(priorities) {
  if (!priorities || priorities.length === 0) return '';
  return `
    <div class="priority-box">
      <h4>🎯 Top Improvement Priorities</h4>
      ${priorities.map((p, i) => `
        <div class="priority-item">
          <span class="priority-number">${i + 1}</span>
          <div class="priority-text">
            <span class="priority-dim">${p.dimension} (${p.score.toFixed(1)}/12${p.gap_to_10 ? ` · ${p.gap_to_10.toFixed(1)} pts to CLB 10` : ''})</span> — ${p.action}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderLevelAdvice(advice) {
  if (!advice) return '';
  return `
    <div class="level-advice-box">
      <h4>📚 Coaching Advice for Your Level</h4>
      <p>${advice}</p>
    </div>
  `;
}

function renderFeedbackCards(feedback) {
  const dimensions = ['content_coherence', 'vocabulary', 'listenability', 'task_fulfillment'];
  return `
    <div class="feedback-section">
      <h3 style="margin-bottom: 16px;">Detailed Feedback</h3>
      ${dimensions.map(dim => {
        const fb = feedback[dim];
        if (!fb) return '';
        return `
          <div class="feedback-card">
            <h4>${fb.criterion} — ${fb.score ? fb.score.toFixed(1) : '—'}/12</h4>
            ${fb.detail ? `<p style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 12px;">${fb.detail}</p>` : ''}
            ${fb.strengths && fb.strengths.length > 0 ? `
              <ul class="feedback-list strengths">
                ${fb.strengths.map(s => `<li>${s}</li>`).join('')}
              </ul>
            ` : ''}
            ${fb.improvements && fb.improvements.length > 0 ? `
              <ul class="feedback-list improvements" style="margin-top: 8px;">
                ${fb.improvements.map(s => `<li>${s}</li>`).join('')}
              </ul>
            ` : ''}
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function renderTranscript(transcript) {
  if (!transcript) return '';
  return `
    <div class="transcript-box">
      <div class="label">Your Transcript</div>
      ${transcript}
    </div>
  `;
}

function renderModelAnswer(answer) {
  if (!answer) return '';
  return `
    <div class="model-answer">
      <div class="label">✨ Model Answer Structure</div>
      <p>${answer}</p>
    </div>
  `;
}

// ============================================================
// Task Actions
// ============================================================
function cancelTask() {
  clearInterval(state.prepTimerInterval);
  clearInterval(state.recordTimerInterval);
  
  if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
    state.mediaRecorder.stop();
  }

  state.fullTestMode = false;
  state.currentTask = null;
  
  document.getElementById('taskSelection').classList.remove('hidden');
  document.getElementById('activeTask').classList.remove('active');
  document.getElementById('prepPhase').classList.remove('hidden');
  document.getElementById('recordPhase').classList.add('hidden');
  document.getElementById('resultsPhase').classList.add('hidden');
  
  // Reset ring classes
  document.querySelectorAll('.timer-ring-progress').forEach(el => {
    el.classList.remove('warning', 'danger');
  });
}

async function retryTask() {
  if (state.currentTask) {
    // Get a new prompt for same task
    const res = await fetch(`/api/tasks/${state.currentTask.number}`);
    const data = await res.json();
    state.currentTask = data;
    state.currentPrompt = data.prompt;
    showPrepPhase();
  }
}

// ============================================================
// Full Test
// ============================================================
async function startFullTest() {
  try {
    const res = await fetch('/api/tasks/full-test');
    const data = await res.json();
    
    state.fullTestMode = true;
    state.fullTestTasks = data.tasks;
    state.fullTestIndex = 0;
    state.fullTestResults = [];

    // Switch to practice view to show task flow
    switchView('practice');
    
    state.currentTask = state.fullTestTasks[0];
    state.currentPrompt = state.currentTask.prompt;
    showPrepPhase();
  } catch (e) {
    console.error('Failed to start full test:', e);
  }
}

function showFullTestResults() {
  document.getElementById('prepPhase').classList.add('hidden');
  document.getElementById('recordPhase').classList.add('hidden');
  document.getElementById('resultsPhase').classList.remove('hidden');

  // Calculate averages
  let totals = { content_coherence: 0, vocabulary: 0, listenability: 0, task_fulfillment: 0, overall: 0 };
  let count = 0;

  state.fullTestResults.forEach(r => {
    if (r.scores && !r.scores.error) {
      totals.content_coherence += r.scores.content_coherence || 0;
      totals.vocabulary += r.scores.vocabulary || 0;
      totals.listenability += r.scores.listenability || 0;
      totals.task_fulfillment += r.scores.task_fulfillment || 0;
      totals.overall += r.scores.overall || 0;
      count++;
    }
  });

  if (count > 0) {
    Object.keys(totals).forEach(k => totals[k] = totals[k] / count);
  }

  const clb = Math.round(totals.overall);

  let html = `
    <h2 style="margin-bottom: 24px;">Full Test Complete!</h2>
    <div class="score-dashboard">
      <div class="overall-score">
        <div class="score-circle">
          <div class="score-value">${totals.overall.toFixed(1)}</div>
          <div class="score-label">Average</div>
        </div>
        <div class="clb-badge">CLB Level ${clb}</div>
      </div>
      <div class="dimension-scores">
        ${renderDimensionCard('Content/Coherence', totals.content_coherence)}
        ${renderDimensionCard('Vocabulary', totals.vocabulary)}
        ${renderDimensionCard('Listenability', totals.listenability)}
        ${renderDimensionCard('Task Fulfillment', totals.task_fulfillment)}
      </div>
    </div>
    
    <div class="level-advice-box" style="margin-top: 24px; text-align: left;">
      <h4>📋 Full Test Evaluation Summary</h4>
      <p>You scored an average of <strong>CLB ${clb}</strong> across all 8 tasks. 
      ${clb >= 9 ? 'Excellent work! You are scoring at a very high level. Focus on minor vocabulary enhancements and eliminating any remaining hesitations to reach CLB 10+ consistently.' : 
        clb >= 7 ? 'Good job! You have a solid foundation. To reach CLB 9+, focus on using more complex grammatical structures and reducing filler words like "um" and "uh".' : 
        'Keep practicing! Focus on completing the task requirements fully and improving your fluency by minimizing long pauses.'}
      </p>
    </div>

    <h3 style="margin: 24px 0 16px;">Per-Task Scores</h3>
    <div class="history-list">
      ${state.fullTestResults.map((r, i) => {
        const task = state.fullTestTasks[i];
        const score = r.scores ? r.scores.overall || 0 : 0;
        return `
          <div class="history-item">
            <div class="history-info">
              <span class="history-task">Task ${task.number}: ${task.name}</span>
            </div>
            <span class="history-score">${score.toFixed(1)}</span>
          </div>
        `;
      }).join('')}
    </div>

    <div class="btn-group" style="margin-top: 32px;">
      <button class="btn btn-secondary" onclick="cancelTask()">← Back to Tasks</button>
      <button class="btn btn-primary" onclick="startFullTest()">Retake Full Test</button>
    </div>
  `;

  document.getElementById('resultsContent').innerHTML = html;
  state.fullTestMode = false;
}

// ============================================================
// History
// ============================================================
async function loadHistory() {
  try {
    const res = await fetch('/api/history?limit=20');
    const data = await res.json();
    const list = document.getElementById('historyList');

    if (!data.sessions || data.sessions.length === 0) {
      list.innerHTML = `
        <div class="progress-empty">
          <div class="icon">📋</div>
          <p>No practice sessions yet. Start practicing to see your history!</p>
        </div>
      `;
      return;
    }

    list.innerHTML = data.sessions.map(s => {
      const scores = s.scores || {};
      const overall = scores.overall || 0;
      const date = new Date(s.created_at).toLocaleString();
      return `
        <div class="history-item">
          <div class="history-info">
            <span class="history-task">Task ${s.task_number}: ${getTaskName(s.task_number)}</span>
            <span class="history-date">${date}</span>
          </div>
          <span class="history-score">${overall.toFixed(1)}</span>
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error('Failed to load history:', e);
  }
}

function getTaskName(num) {
  const names = {
    0: 'Practice (Unscored)', 1: 'Giving Advice', 2: 'Personal Experience', 3: 'Describing a Scene',
    4: 'Making Predictions', 5: 'Comparing & Persuading', 6: 'Difficult Situation',
    7: 'Expressing Opinions', 8: 'Unusual Situation'
  };
  return names[num] || `Task ${num}`;
}

// ============================================================
// Progress
// ============================================================
async function loadProgress() {
  try {
    const res = await fetch('/api/progress');
    const data = await res.json();
    const content = document.getElementById('progressContent');

    if (!data.progress || data.progress.length === 0) {
      content.innerHTML = `
        <div class="progress-empty">
          <div class="icon">📊</div>
          <p>Complete some practice sessions to track your progress over time!</p>
        </div>
      `;
      return;
    }

    // Simple text-based progress display
    const latest = data.progress[data.progress.length - 1];
    const first = data.progress[0];
    const latestScores = latest.scores;
    const firstScores = first.scores;

    const dimensions = ['content_coherence', 'vocabulary', 'listenability', 'task_fulfillment', 'overall'];
    const labels = { 
      content_coherence: 'Content/Coherence', vocabulary: 'Vocabulary', 
      listenability: 'Listenability', task_fulfillment: 'Task Fulfillment', overall: 'Overall'
    };

    content.innerHTML = `
      <div class="card" style="margin-bottom: 16px;">
        <h3 style="margin-bottom: 16px;">📊 Score Summary (${data.total_sessions} sessions)</h3>
        <div class="dimension-scores">
          ${dimensions.map(dim => {
            const current = latestScores[dim] || 0;
            const initial = firstScores[dim] || 0;
            const change = current - initial;
            const changeText = change > 0 ? `↑ ${change.toFixed(1)}` : change < 0 ? `↓ ${Math.abs(change).toFixed(1)}` : '—';
            const changeColor = change > 0 ? 'var(--accent-success)' : change < 0 ? 'var(--accent-danger)' : 'var(--text-muted)';
            return `
              <div class="dimension-card">
                <div class="dimension-header">
                  <span class="dimension-name">${labels[dim]}</span>
                  <span class="dimension-score">${current.toFixed(1)}</span>
                </div>
                <div class="score-bar-bg">
                  <div class="score-bar-fill ${current >= 9 ? 'good' : current >= 6 ? 'warning' : 'danger'}" style="width: ${(current/12)*100}%"></div>
                </div>
                <div style="font-size: 0.8rem; color: ${changeColor};">${changeText} since first session</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  } catch (e) {
    console.error('Failed to load progress:', e);
  }
}
