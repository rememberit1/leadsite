// GET /api/stats?days=7 with header "Authorization: Bearer <STATS_TOKEN>" -> daily lead/call-click counts for the daily report.
export async function onRequestGet({ request, env }) {
  if (!env.STATS_TOKEN || request.headers.get("authorization") !== `Bearer ${env.STATS_TOKEN}`)
    return new Response("Unauthorized", { status: 401 });
  const days = Math.min(parseInt(new URL(request.url).searchParams.get("days") || "7", 10), 90);
  const out = [];
  for (let i = 0; i < days; i++) {
    const d = new Date(Date.now() - i * 864e5).toISOString().slice(0, 10);
    out.push({ date: d, leads: +(await env.LEADS.get(`count:leads:${d}`) || 0), call_clicks: +(await env.LEADS.get(`count:calls:${d}`) || 0) });
  }
  const recent = await env.LEADS.list({ prefix: `lead:${out[0].date}` });
  return Response.json({ days: out, leads_today_keys: recent.keys.map(k => k.name) });
}
