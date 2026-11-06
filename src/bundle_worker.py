#!/usr/bin/env python3
"""Bundle public/ into dist/_worker.js and write dist/deploy.js (code for the Cloudflare MCP execute tool)."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public"); DIST = os.path.join(ROOT, "dist"); os.makedirs(DIST, exist_ok=True)
files = {}
for d, _, fs in os.walk(PUB):
    for f in fs:
        if f == "_headers": continue
        full = os.path.join(d, f); files[os.path.relpath(full, PUB)] = open(full).read()
worker = open(os.path.join(ROOT, "src", "worker_template.js")).read().replace("__FILES__", json.dumps(files))
open(os.path.join(DIST, "_worker.js"), "w").write(worker)
deploy = """async () => {
  const worker = %s;
  const b = 'LEADSITE' + Date.now();
  const part = (name, ctype, data, filename) => [`--${b}`, `Content-Disposition: form-data; name="${name}"` + (filename ? `; filename="${filename}"` : ''), `Content-Type: ${ctype}`, '', data].join('\\r\\n');
  const body = [part('manifest', 'application/json', '{}'), part('branch', 'text/plain', 'main'),
                part('_worker.js', 'application/javascript+module', worker, '_worker.js'), `--${b}--`, ''].join('\\r\\n');
  const r = await cloudflare.request({ method: 'POST', path: `/accounts/${accountId}/pages/projects/silverspring-plumbing-pros/deployments`, body, contentType: `multipart/form-data; boundary=${b}`, rawBody: true });
  return { id: r.result?.id, url: r.result?.url, stage: r.result?.latest_stage, aliases: r.result?.aliases, env: r.result?.environment };
}""" % json.dumps(worker)
open(os.path.join(DIST, "deploy.js"), "w").write(deploy)
print(f"{len(files)} files, worker {len(worker)//1024} KB")
