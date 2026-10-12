import {api} from '../services/api.js?v=20261012-01';
import {workflows, initialState} from '../features/workflows.js?v=20261012-01';
import {escapeHtml as esc} from '../utils/escape-html.js?v=20261012-01';

const content = document.querySelector('#content');
const notice = document.querySelector('#notice');
const refs = new Map();
let busy = false;
function message(text) { notice.hidden = !text; notice.textContent = text; }
function threadFor(id) {
  if (refs.has(id)) return refs.get(id);
  try { return localStorage.getItem(`teacher-agent:${id}:thread`) || ''; } catch { return ''; }
}
function saveThread(id, thread) {
  refs.set(id, thread);
  try { localStorage.setItem(`teacher-agent:${id}:thread`, thread); } catch { /* Memory fallback. */ }
}
const links = [['home', '成长首页'], ...workflows.map(w => [w.id, w.title]),
  ['knowledge', '知识资料'], ['evaluation', '综合评价'], ['profile', '成长画像']];
function route() { return location.hash.slice(1) || 'home'; }
function render() {
  if (busy) return;
  const selected = route();
  document.querySelector('#nav').innerHTML = links.map(([id, title]) =>
    `<a href="#${id}" ${selected === id ? 'aria-current="page"' : ''}>${title}</a>`).join('');
  message('');
  const wf = workflows.find(w => w.id === selected);
  if (wf) return renderWorkflow(wf);
  if (selected === 'knowledge') {
    content.innerHTML = '<h1>知识资料</h1><p class="lead">将教学材料提交到知识库，供后续工具检索。</p><form id="upload" class="panel"><label>选择文档<input name="file" type="file" accept=".pdf,.docx,.vsdx,.txt,.md" required></label><button>上传并入库</button><p>支持 PDF、DOCX、VSDX、TXT、Markdown；入库需要后端模型和数据库服务。</p></form><pre id="upload-result" hidden></pre>';
    document.querySelector('#upload').onsubmit = e => {
      e.preventDefault(); const file = new FormData(e.currentTarget).get('file');
      run(async () => { const result = await api.ingest(file); const box = document.querySelector('#upload-result'); box.hidden = false; box.textContent = JSON.stringify(result, null, 2); message('入库请求已返回，请查看结果。'); });
    };
    return;
  }
  if (['evaluation', 'profile'].includes(selected)) {
    content.innerHTML = `<h1>${selected === 'evaluation' ? '综合评价' : '成长画像'}</h1><div class="panel empty"><h2>等待业务服务接入</h2><p>当前尚未提供此页面所需的查询接口。工作流候选结果不会在这里作为正式评价或能力分数展示。</p><a href="#home">返回成长首页</a></div>`;
    return;
  }
  content.innerHTML = `<div class="hero"><div><p class="eyebrow">TEACHER DEVELOPMENT</p><h1>让每次实践，成为成长的证据</h1><p class="lead">明确目标、设计教学、开展实践、反思迁移。选择一个阶段开始。</p></div><img src="/web/public/assets/mascots/cnu-mascot.png" alt="教师成长吉祥物"></div><div class="cards">${workflows.map((w, i) => `<a class="panel stage-card" href="#${w.id}"><span class="number">0${i + 1}</span><h2>${w.title}</h2><p>${w.subtitle}</p><span>${threadFor(w.id) ? '查看已有任务 →' : '进入工作区 →'}</span></a>`).join('')}</div><div class="panel"><h2>从真实任务开始</h2><p>先准备教学材料和已有证据。工作台显示后端返回的实际状态；执行结果是否达到业务要求，仍需负责人确认。</p></div>`;
}

function renderWorkflow(wf) {
  const thread = threadFor(wf.id);
  content.innerHTML = `<p class="eyebrow">教师成长 / ${wf.title}</p><h1>${wf.title}</h1><p class="lead">${wf.subtitle}</p><div class="workspace"><section class="panel"><h2>开始新任务</h2><form id="start">${wf.fields.map(([key, title, placeholder]) => `<label>${title}<textarea name="${key}" placeholder="${placeholder}" maxlength="12000" required rows="3"></textarea></label>`).join('')}<button>创建并开始</button></form><hr><form id="lookup"><label>已有任务编号<input name="thread" value="${esc(thread)}" maxlength="128" required></label><button class="secondary">查询任务状态</button></form><p class="hint">只在此设备保存任务编号，不保存输入正文。连接中断后可用编号重新查询。</p></section><section class="panel"><h2>任务结果与待办</h2><div id="result" aria-live="polite"><p class="empty">开始任务或输入已有编号，查看状态。</p></div></section></div>`;
  document.querySelector('#start').onsubmit = e => {
    e.preventDefault(); const state = initialState(wf.id, new FormData(e.currentTarget));
    const id = `${wf.id}-${crypto.randomUUID()}`;
    saveThread(wf.id, id);
    document.querySelector('[name="thread"]').value = id;
    run(async () => { await api.start(wf.name, id, state); showResult(wf, id, await api.status(wf.name, id)); });
  };
  document.querySelector('#lookup').onsubmit = e => {
    e.preventDefault(); const id = String(new FormData(e.currentTarget).get('thread')).trim();
    if (!id) return;
    run(async () => { const snapshot = await api.status(wf.name, id); saveThread(wf.id, id); showResult(wf, id, snapshot); });
  };
}

function showResult(wf, id, snapshot) {
  const state = snapshot.values || {};
  const pending = Array.isArray(snapshot.interrupts) ? snapshot.interrupts : [];
  const results = Object.entries(state.artifacts || {});
  const hasState = Object.keys(state).length > 0;
  // Do not infer successful completion merely from an empty next-node list.
  document.querySelector('#result').innerHTML = `<p><strong>任务编号：</strong>${esc(id)}</p><p><strong>状态：</strong>${pending.length ? '等待人工确认' : hasState ? esc(state.status || '状态已返回') : '未找到已保存状态'}</p><p><strong>当前步骤：</strong>${esc(state.current_stage || state.current_node || '暂无')}</p><p>待执行节点：${esc((snapshot.next || []).join('、') || '无')}。无待执行节点不代表业务验收通过。</p>${pending.length ? `<form id="resume"><h3>待确认内容</h3><pre>${esc(JSON.stringify(pending, null, 2))}</pre><label>处理意见<textarea name="comment" required rows="3"></textarea></label><label>选择决定<select name="action"><option value="confirm">确认</option><option value="revise">请求修改</option></select></label><button>提交意见并继续</button><p class="hint">意见交给后端处理，是否修改流程取决于该节点已实现的规则。</p></form>` : ''}<h3>候选产物（${results.length}）</h3>${results.length ? results.map(([key, item]) => `<details><summary>${esc(key)} · ${esc(item?.status || '候选记录')}</summary><pre>${esc(JSON.stringify(item, null, 2))}</pre></details>`).join('') : '<p>尚无产物记录。</p>'}`;
  const form = document.querySelector('#resume');
  if (form) form.onsubmit = e => {
    e.preventDefault(); const data = new FormData(e.currentTarget);
    run(async () => { await api.resume(wf.name, id, {action: data.get('action'), comment: data.get('comment')}); showResult(wf, id, await api.status(wf.name, id)); });
  };
  message('已读取后端任务状态。');
}

async function run(action) {
  if (busy) return;
  const originalRoute = route(); busy = true;
  content.querySelectorAll('button').forEach(button => { button.disabled = true; });
  content.setAttribute('aria-busy', 'true'); message('正在处理，请稍候…');
  try { await action(); } catch (error) { message(error.message || '连接失败，请检查后端服务。'); }
  finally {
    busy = false; content.removeAttribute('aria-busy');
    content.querySelectorAll('button').forEach(button => { button.disabled = false; });
    if (route() !== originalRoute) render();
  }
}
window.addEventListener('hashchange', render);
render();
api.health().then(() => { document.querySelector('#connection').textContent = '服务已连接'; })
  .catch(() => { document.querySelector('#connection').textContent = '服务未连接'; });
