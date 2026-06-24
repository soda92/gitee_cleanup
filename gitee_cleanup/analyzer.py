import json
import os
from .config import Config

def parse_graphql_from_har(har_path):
    with open(har_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("log", {}).get("entries", [])
    graphql_entries = []

    for idx, entry in enumerate(entries):
        req = entry.get("request", {})
        url = req.get("url", "")
        if "graphql" in url.lower():
            graphql_entries.append((idx, entry))
    return graphql_entries

def generate_report():
    config = Config()
    har_path = config.har
    out_path = config.report

    print(f"Reading HAR file from: {har_path}")
    if not os.path.exists(har_path):
        print(f"Error: HAR file does not exist at {har_path}")
        return

    graphql_entries = parse_graphql_from_har(har_path)
    
    md_lines = []
    md_lines.append("# GraphQL Requests Analysis")
    md_lines.append(f"Parsed from `{os.path.basename(har_path)}`. Found **{len(graphql_entries)}** GraphQL requests.\n")

    md_lines.append("## Overview Table\n")
    md_lines.append("| Index | Method | Operation | Status | URL |")
    md_lines.append("|-------|--------|-----------|--------|-----|")

    for idx, entry in graphql_entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})
        
        post_data = req.get("postData", {})
        post_text = post_data.get("text", "")
        
        operation_name = "N/A"
        try:
            parsed_post = json.loads(post_text)
            if isinstance(parsed_post, dict):
                operation_name = parsed_post.get("operationName") or "N/A"
            elif isinstance(parsed_post, list):
                operation_name = ", ".join([item.get("operationName") or "N/A" for item in parsed_post])
        except Exception:
            pass
            
        status = f"{resp.get('status')} {resp.get('statusText')}"
        md_lines.append(f"| {idx} | {req.get('method')} | `{operation_name}` | {status} | `{req.get('url')}` |")

    md_lines.append("\n---\n")
    md_lines.append("## Detailed Request & Response Logs\n")

    for idx, entry in graphql_entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})
        
        post_data = req.get("postData", {})
        post_text = post_data.get("text", "")
        
        resp_content = resp.get("content", {})
        resp_text = resp_content.get("text", "")
        
        operation_name = "N/A"
        query = ""
        variables = None
        try:
            parsed_post = json.loads(post_text)
            if isinstance(parsed_post, dict):
                operation_name = parsed_post.get("operationName") or "N/A"
                query = parsed_post.get("query", "")
                variables = parsed_post.get("variables")
            elif isinstance(parsed_post, list):
                operation_name = "Batch: " + ", ".join([item.get("operationName") or "N/A" for item in parsed_post])
        except Exception:
            pass
            
        md_lines.append(f"### Entry #{idx}: Operation `{operation_name}`")
        md_lines.append(f"- **URL**: `{req.get('url')}`")
        md_lines.append(f"- **Status**: `{resp.get('status')} {resp.get('statusText')}`")
        md_lines.append(f"- **Duration**: `{entry.get('time', 0):.2f} ms`")
        
        md_lines.append("\n#### Request Query")
        if query:
            md_lines.append("```graphql")
            md_lines.append(query.strip())
            md_lines.append("```")
        else:
            md_lines.append("```json")
            md_lines.append(post_text.strip())
            md_lines.append("```")
            
        if variables:
            md_lines.append("\n#### Request Variables")
            md_lines.append("```json")
            md_lines.append(json.dumps(variables, indent=2, ensure_ascii=False))
            md_lines.append("```")
            
        md_lines.append("\n#### Response Data")
        try:
            parsed_resp = json.loads(resp_text)
            md_lines.append("```json")
            md_lines.append(json.dumps(parsed_resp, indent=2, ensure_ascii=False))
            md_lines.append("```")
        except Exception:
            if resp_text:
                md_lines.append("```json")
                md_lines.append(resp_text.strip())
                md_lines.append("```")
            else:
                md_lines.append("*Empty response body*")
                
        md_lines.append("\n---\n")

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Generated analysis report at: {out_path}")
