# utils/prompt_loader.py
from pathlib import Path

class PromptLoader:
    def __init__(self, prompts_dir: Path):
        self.prompts_dir = prompts_dir
        self.analysis_prompt = ""
        self.fullfix_prompt = ""
        self.reload()

    def reload(self):
        analysis_file = self.prompts_dir / "analysisPrompt.txt"
        fullfix_file = self.prompts_dir / "fullFixPrompt.txt"
        if not analysis_file.exists() or not fullfix_file.exists():
            raise FileNotFoundError("Prompts not found in prompts/ directory.")
        self.analysis_prompt = analysis_file.read_text(encoding="utf-8")
        self.fullfix_prompt = fullfix_file.read_text(encoding="utf-8")
