// Cloudflare Pages Function: POST /api/lead -> store lead in KV (binding LEADS), redirect to /thank-you/
export async function onRequestPost({ request, env }) {
  const form = await request.formData();
  if (form.get("company")) return Response.redirect(new URL("/thank-you/", request.url), 303); // honeypot
  const clean = (k, n = 200) => String(form.get(k) || "").trim().slice(0, n);
  const lead = {
    name: clean("name", 100), phone: clean("phone", 30), zip: clean("zip", 10),
    service: clean("service", 80), message: clean("message", 2000), page: clean("page", 200),
    ts: new Date().toISOString(), ip_country: request.cf?.country || null,
    ua: (request.headers.get("user-agent") || "").slice(0, 200),
  };
  if (!lead.name || !lead.phone) return new Response("Name and phone are required.", { status: 400 });
  const day = lead.ts.slice(0, 10);
  await env.LEADS.put(`lead:${day}:${crypto.randomUUID()}`, JSON.stringify(lead));
  const c = parseInt((await env.LEADS.get(`count:leads:${day}`)) || "0", 10);
  await env.LEADS.put(`count:leads:${day}`, String(c + 1));
  return Response.redirect(new URL("/thank-you/", request.url), 303);
}
export const onRequestGet = () => new Response("Method not allowed", { status: 405 });
