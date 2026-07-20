const REPOSITORY = 'pri8771/studio-ios';
const NEW_TASK_URL = `https://github.com/${REPOSITORY}/issues/new?template=studio-task.yml`;

function esc(value) {
  return String(value ?? '—').replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

function badge(value) {
  const slug = String(value ?? 'unknown').toLowerCase().replace(/[^a-z0-9]+/g, '-');
  return `<span class="badge ${slug}">${esc(value ?? 'unknown')}</span>`;
}

function renderTaskRows(tasks) {
  const body = document.querySelector('#task-issue-rows');
  if (!tasks.length) {
    body.innerHTML = '<tr><td colspan="8">No Studio task issues yet.</td></tr>';
    return;
  }
  body.innerHTML = tasks.map(task => `<tr>
    <td><a href="${esc(task.url)}" target="_blank" rel="noreferrer"><strong>#${task.number} ${esc(task.title)}</strong></a><small>${esc(task.objective)}</small></td>
    <td>${badge(task.product)}</td>
    <td>${badge(task.owner)}</td>
    <td>${badge(task.priority)}</td>
    <td>${badge(task.status)}</td>
    <td>${esc(task.dueDate)}</td>
    <td>${esc(task.approvalGate)}</td>
    <td><a class="button secondary" href="${esc(task.url)}" target="_blank" rel="noreferrer">Open</a></td>
  </tr>`).join('');
}

function renderTaskSummary(summary) {
  const values = {
    'command-open': summary.open,
    'command-running': summary.running,
    'command-blocked': summary.blocked,
    'command-approvals': summary.approvalNeeded,
  };
  Object.entries(values).forEach(([id, value]) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value ?? 0;
  });
}

async function loadTasks() {
  try {
    const response = await fetch('./task-issues.json', {cache: 'no-store'});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const snapshot = await response.json();
    renderTaskRows(snapshot.tasks ?? []);
    renderTaskSummary(snapshot.summary ?? {});
    const freshness = document.querySelector('#task-freshness');
    if (freshness) freshness.textContent = snapshot.tokenAvailable
      ? `Synced ${new Date(snapshot.generatedAt).toLocaleString()}`
      : 'Local snapshot; GitHub sync requires GITHUB_TOKEN.';
  } catch (error) {
    document.querySelector('#task-issue-rows').innerHTML = `<tr><td colspan="8">Task sync unavailable: ${esc(error)}</td></tr>`;
  }
}

function setupControls() {
  document.querySelectorAll('[data-new-task]').forEach(button => {
    button.addEventListener('click', () => window.open(NEW_TASK_URL, '_blank', 'noopener'));
  });
  const approvalButton = document.querySelector('[data-approval-queue]');
  if (approvalButton) {
    approvalButton.addEventListener('click', () => window.open(`https://github.com/${REPOSITORY}/issues?q=is%3Aissue+is%3Aopen+label%3Astudio-task+label%3Astatus%3Aapproval-needed`, '_blank', 'noopener'));
  }
}

setupControls();
loadTasks();
