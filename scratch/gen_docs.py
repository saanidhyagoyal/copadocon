import json
import os

with open('scratch/openapi.json') as f:
    spec = json.load(f)

schemas = spec.get('components', {}).get('schemas', {})
paths = spec.get('paths', {})

def resolve_ref(ref_str):
    parts = ref_str.replace('#/', '').split('/')
    obj = spec
    for p in parts:
        obj = obj.get(p, {})
    return obj

def join_pipe(items):
    return ' | '.join(items)

def get_category(path):
    parts = path.strip('/').split('/')
    meaningful = []
    for p in parts:
        if p.startswith('{'):
            continue
        if p == 'organizations':
            continue
        meaningful.append(p)
    if meaningful:
        return meaningful[0].replace('-', ' ').replace('_', ' ').title()
    return 'General'

def get_field_type(fval):
    if '$ref' in fval:
        return fval['$ref'].split('/')[-1]
    elif 'anyOf' in fval:
        ftypes = []
        for v in fval['anyOf']:
            if '$ref' in v:
                ftypes.append(v['$ref'].split('/')[-1])
            elif v.get('type') == 'null':
                ftypes.append('null')
            elif v.get('type') == 'array':
                items = v.get('items', {})
                if '$ref' in items:
                    ftypes.append('array[' + items['$ref'].split('/')[-1] + ']')
                else:
                    ftypes.append('array[' + items.get('type','?') + ']')
            else:
                ftypes.append(v.get('type', '?'))
        sep = ' \\| '
        return sep.join(ftypes)
    elif fval.get('type') == 'array':
        items = fval.get('items', {})
        if '$ref' in items:
            return 'array[' + items['$ref'].split('/')[-1] + ']'
        else:
            return 'array[' + items.get('type','?') + ']'
    else:
        ftype = fval.get('type', 'unknown')
        fmt = fval.get('format', '')
        if fmt:
            ftype += ' (' + fmt + ')'
        return ftype

def get_response_schema(rs):
    if '$ref' in rs:
        return '`' + rs['$ref'].split('/')[-1] + '`'
    elif rs.get('type') == 'array' and 'items' in rs:
        items = rs['items']
        if '$ref' in items:
            return 'array[`' + items['$ref'].split('/')[-1] + '`]'
        else:
            return 'array[`' + items.get('type','?') + '`]'
    else:
        return '`' + rs.get('type', 'object') + '`'

# Group endpoints by category
categories = {}
for path, methods in paths.items():
    cat = get_category(path)
    if cat not in categories:
        categories[cat] = []
    for method, op in methods.items():
        categories[cat].append((method.upper(), path, op))

md = []
md.append("# 🚀 CopadoGPT Gateway API — Complete Endpoint Reference")
md.append("")
md.append("> **API Version:** " + spec['info']['version'])
md.append("> **Base URL:** `https://copadogpt-api.robotic.copado.com`")
md.append("> **Spec:** OpenAPI 3.1.0 (FastAPI)")
md.append("> **Total Endpoints:** " + str(sum(len(v) for v in categories.values())))
md.append("> **Total Schemas:** " + str(len(schemas)))
md.append("")
md.append("---")
md.append("")

# TOC
md.append("## 📋 Table of Contents")
md.append("")
toc_idx = 1
for cat in categories:
    anchor = cat.lower().replace(' ', '-').replace('/', '-')
    count = len(categories[cat])
    md.append(str(toc_idx) + ". [" + cat + " (" + str(count) + " endpoints)](#" + anchor + ")")
    toc_idx += 1
md.append(str(toc_idx) + ". [Schema / Model Reference](#schema--model-reference)")
md.append("")
md.append("---")
md.append("")

# Auth
md.append("## 🔐 Authentication")
md.append("")
md.append("Most endpoints require authentication via one or more of the following methods:")
md.append("")
md.append("| Method | Type | Details |")
md.append("|--------|------|---------|")
md.append("| `apikey` | API Key | Primary API key authentication |")
md.append("| `apikey2` | API Key | Secondary/alternate API key |")
md.append("| `cookie_auth` | Cookie | Session-based cookie authentication |")
md.append("| `header_xsrf` | Header | XSRF token in header |")
md.append("| `cookie_xsrf` | Cookie | XSRF token in cookie |")
md.append("")
md.append("---")
md.append("")

# Common headers
md.append("## 📨 Common Headers")
md.append("")
md.append("| Header | Type | Required | Description |")
md.append("|--------|------|----------|-------------|")
md.append("| `x-client` | `string` | No | Client identifier for tracking |")
md.append("| `Content-Type` | `string` | Yes (for POST/PATCH) | `application/json` or `multipart/form-data` |")
md.append("")
md.append("---")
md.append("")

# Endpoints by category
for cat, endpoints in categories.items():
    md.append("## " + cat)
    md.append("")
    
    for method, path, op in endpoints:
        summary = op.get('summary', 'N/A')
        desc = op.get('description', '')
        
        badge = {'GET': '🟢', 'POST': '🔵', 'PATCH': '🟡', 'PUT': '🟠', 'DELETE': '🔴'}.get(method, '⚪')
        
        md.append("### " + badge + " `" + method + "` `" + path + "`")
        md.append("")
        md.append("**" + summary + "**")
        md.append("")
        if desc:
            # Escape newlines in description
            desc_lines = desc.replace('\n', '\n> ')
            md.append("> " + desc_lines)
            md.append("")
        
        params = op.get('parameters', [])
        path_params = [p for p in params if p.get('in') == 'path']
        query_params = [p for p in params if p.get('in') == 'query']
        
        if path_params:
            md.append("**Path Parameters:**")
            md.append("")
            md.append("| Parameter | Type | Required | Description |")
            md.append("|-----------|------|----------|-------------|")
            for p in path_params:
                pschema = p.get('schema', {})
                ptype = pschema.get('type', 'string')
                pfmt = pschema.get('format', '')
                if pfmt:
                    ptype = ptype + ' (' + pfmt + ')'
                preq = 'Yes' if p.get('required') else 'No'
                pdesc = p.get('description', p['name'].replace('_', ' ').title())
                md.append("| `" + p['name'] + "` | `" + ptype + "` | " + preq + " | " + pdesc + " |")
            md.append("")
        
        if query_params:
            md.append("**Query Parameters:**")
            md.append("")
            md.append("| Parameter | Type | Required | Default | Description |")
            md.append("|-----------|------|----------|---------|-------------|")
            for p in query_params:
                pschema = p.get('schema', {})
                ptype = get_field_type(pschema)
                preq = 'Yes' if p.get('required') else 'No'
                default = str(pschema.get('default', '—'))
                pdesc = p.get('description', '')
                md.append("| `" + p['name'] + "` | `" + ptype + "` | " + preq + " | `" + default + "` | " + pdesc + " |")
            md.append("")
        
        # Request body
        if 'requestBody' in op:
            rb = op['requestBody']
            md.append("**Request Body" + (" (required)" if rb.get('required') else "") + ":**")
            md.append("")
            for ct, cv in rb.get('content', {}).items():
                md.append("Content-Type: `" + ct + "`")
                md.append("")
                if 'schema' in cv:
                    s = cv['schema']
                    if '$ref' in s:
                        ref_name = s['$ref'].split('/')[-1]
                        md.append("Schema: [`" + ref_name + "`](#" + ref_name.lower().replace(' ', '-') + ")")
                        md.append("")
                        resolved = resolve_ref(s['$ref'])
                        props = resolved.get('properties', {})
                        req_fields = resolved.get('required', [])
                        if props:
                            md.append("| Field | Type | Required | Description |")
                            md.append("|-------|------|----------|-------------|")
                            for fname, fval in props.items():
                                freq = "✅ Yes" if fname in req_fields else "No"
                                ftype = get_field_type(fval)
                                fdesc = (fval.get('description', '') or '')[:120]
                                fdefault = fval.get('default', '')
                                if fdefault != '':
                                    fdesc += " (default: `" + str(fdefault) + "`)"
                                md.append("| `" + fname + "` | `" + ftype + "` | " + freq + " | " + fdesc + " |")
                            md.append("")
                            
                            # Generate example JSON
                            md.append("<details>")
                            md.append("<summary>📝 Example Request JSON</summary>")
                            md.append("")
                            md.append("```json")
                            example = {}
                            for fname, fval in props.items():
                                ft = get_field_type(fval)
                                if 'string' in ft:
                                    if 'uuid' in ft:
                                        example[fname] = "00000000-0000-0000-0000-000000000000"
                                    elif 'date-time' in ft:
                                        example[fname] = "2025-01-01T00:00:00Z"
                                    elif 'email' in ft:
                                        example[fname] = "user@example.com"
                                    else:
                                        example[fname] = "string"
                                elif 'integer' in ft:
                                    example[fname] = 0
                                elif 'number' in ft:
                                    example[fname] = 0.0
                                elif 'boolean' in ft:
                                    example[fname] = False if fval.get('default') is None else fval.get('default')
                                elif 'array' in ft:
                                    example[fname] = []
                                elif 'null' in ft:
                                    example[fname] = None
                                elif 'object' in ft:
                                    example[fname] = {}
                                else:
                                    example[fname] = "..."
                                # Use default if available
                                if fval.get('default') is not None and fval.get('default') != '':
                                    example[fname] = fval['default']
                            md.append(json.dumps(example, indent=2))
                            md.append("```")
                            md.append("")
                            md.append("</details>")
                            md.append("")
                    else:
                        stype = s.get('type', 'object')
                        md.append("Type: `" + stype + "`")
                        if s.get('additionalProperties'):
                            md.append("*(accepts any JSON object)*")
                        md.append("")
        
        # Responses
        responses = op.get('responses', {})
        if responses:
            md.append("**Responses:**")
            md.append("")
            md.append("| Status | Description | Response Schema |")
            md.append("|--------|-------------|-----------------|")
            for status_code, resp in responses.items():
                rdesc = resp.get('description', '')
                content = resp.get('content', {})
                if content:
                    for rct, rcv in content.items():
                        if 'schema' in rcv:
                            rschema = get_response_schema(rcv['schema'])
                        else:
                            rschema = '—'
                else:
                    rschema = '—'
                md.append("| `" + str(status_code) + "` | " + rdesc + " | " + rschema + " |")
            md.append("")
        
        md.append("---")
        md.append("")

# Schema reference
md.append("## Schema / Model Reference")
md.append("")
md.append("Below are **all " + str(len(schemas)) + " data models** (schemas) used across the API.")
md.append("")

for sname in sorted(schemas.keys()):
    s = schemas[sname]
    md.append("### `" + sname + "`")
    md.append("")
    
    if s.get('description'):
        desc_clean = s['description'].replace('\n', ' ')
        md.append("> " + desc_clean)
        md.append("")
    
    if 'enum' in s:
        md.append("**Type:** Enum (`" + s.get('type', 'string') + "`)")
        md.append("")
        md.append("**Values:**")
        for v in s['enum']:
            md.append("- `" + str(v) + "`")
        md.append("")
    elif 'const' in s:
        md.append("**Const:** `" + str(s['const']) + "`")
        md.append("")
    elif 'properties' in s:
        props = s.get('properties', {})
        req_fields = s.get('required', [])
        md.append("| Field | Type | Required | Description |")
        md.append("|-------|------|----------|-------------|")
        for fname, fval in props.items():
            freq = "✅" if fname in req_fields else "—"
            ftype = get_field_type(fval)
            fdesc = (fval.get('description', '') or '')[:150]
            fdefault = fval.get('default', '')
            if fdefault != '':
                fdesc += " (default: `" + str(fdefault) + "`)"
            md.append("| `" + fname + "` | `" + ftype + "` | " + freq + " | " + fdesc + " |")
        md.append("")
    elif 'anyOf' in s or 'oneOf' in s:
        variants = s.get('anyOf') or s.get('oneOf', [])
        md.append("**Union type — one of:**")
        md.append("")
        for v in variants:
            if '$ref' in v:
                md.append("- `" + v['$ref'].split('/')[-1] + "`")
            else:
                md.append("- `" + v.get('type', 'unknown') + "`")
        md.append("")
    else:
        md.append("Type: `" + s.get('type', 'object') + "`")
        md.append("")

output = '\n'.join(md)
with open('agentread.md', 'w') as f:
    f.write(output)

print("Generated agentread.md with " + str(len(md)) + " lines")
print("Total endpoints documented: " + str(sum(len(v) for v in categories.values())))
print("Total schemas documented: " + str(len(schemas)))
print("Categories: " + str(list(categories.keys())))
print("File size: " + str(len(output)) + " bytes")
