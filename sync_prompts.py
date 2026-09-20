from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
for name in ['prescription-extraction.txt','extraction-schema.json']:
 shutil.copy(root/'prompts'/name,root/'app/src/main/assets'/name)
