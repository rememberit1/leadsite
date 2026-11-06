// POST /api/call-click -> count tel: link clicks per day in KV (binding LEADS).
// This approximates call intent only; real call counts require a call-tracking number.
export async function onRequestPost({ request, env }) {
  let page = "";
  try { page = String((await request.json()).page || "").slice(0, 200); } catch (_) {}
  const day = new Date().toISOString().slice(0, 10);
  const key = `count:calls:${day}`;
  const c = parseInt((await env.LEADS.get(key)) || "0", 10);
  await env.LEADS.put(key, String(c + 1));
  await env.LEADS.put(`call:${day}:${crypto.randomUUID()}`, JSON.stringify({ page, ts: new Date().toISOString() }), { expirationTtl: 60 * 60 * 24 * 90 });
  return new Response(null, { status: 204 });
}
