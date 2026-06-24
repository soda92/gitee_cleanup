import json
import os

class Config:
    def __init__(self):
        # Default paths relative to workspace root
        self.har_path = "resources/gitee.com.har"
        self.html_path = "resources/工作台 - Gitee.com.html"
        self.output_report_path = "graphql_requests_analysis.md"
        
        # Resolve config.json location
        config_path = os.path.join(os.getcwd(), "config.json")
        if not os.path.exists(config_path):
            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(os.path.dirname(pkg_dir), "config.json")
            
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.har_path = data.get("har_path", self.har_path)
                    self.html_path = data.get("html_path", self.html_path)
                    self.output_report_path = data.get("output_report_path", self.output_report_path)
            except Exception as e:
                print(f"Warning: Failed to load config.json: {e}")

    def get_resolved_path(self, path_str):
        if os.path.isabs(path_str):
            return path_str
        return os.path.abspath(path_str)

    @property
    def har(self):
        return self.get_resolved_path(self.har_path)

    @property
    def html(self):
        return self.get_resolved_path(self.html_path)

    @property
    def report(self):
        return self.get_resolved_path(self.output_report_path)
