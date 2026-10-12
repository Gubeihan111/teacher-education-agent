const base = '/api/v1';

async function request(path, options = {}) {
  // A timeout does not mean the backend task stopped. Never automatically retry writes.
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120000);
  try {
    const response = await fetch(base + path, {...options, signal: controller.signal});
    const text = await response.text();
    let body;
    try { body = JSON.parse(text); } catch { body = null; }
    if (!response.ok) {
      const detail = body?.detail;
      throw new Error(`请求失败（${response.status}）：${typeof detail === 'string' ? detail : detail ? JSON.stringify(detail) : '请查看服务日志'}`);
    }
    if (body === null) throw new Error('服务没有返回有效数据，请检查 API 地址。');
    return body;
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('请求等待超时，后台可能仍在处理。请查询此任务状态，不要重复开始。');
    throw error;
  } finally { clearTimeout(timeout); }
}

function post(path, body) {
  return request(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
}
export const api = {
  health: () => request('/health'),
  start: (name, thread, state) => post(`/workflows/${encodeURIComponent(name)}/start`, {thread_id: thread, state}),
  resume: (name, thread, decision) => post(`/workflows/${encodeURIComponent(name)}/resume`, {thread_id: thread, decision}),
  status: (name, thread) => request(`/workflows/${encodeURIComponent(name)}/${encodeURIComponent(thread)}`),
  ingest: file => { const data = new FormData(); data.append('file', file); return request('/knowledge/ingest', {method: 'POST', body: data}); }
};
