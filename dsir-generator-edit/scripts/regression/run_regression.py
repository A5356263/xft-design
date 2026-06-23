import subprocess
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
examples = []

generic = root / 'assets' / 'examples' / 'list_management_example_dsir.json'
if generic.exists():
    examples.append(('generic-shape', [sys.executable, str(root / 'scripts' / 'check_output_shape.py'), str(generic)]))
    examples.append(('generic-validate', [sys.executable, str(root / 'scripts' / 'validate_dsir.py'), str(generic)]))

genux = root / 'assets' / 'examples' / 'genux-compile-tax-reimbursement-like' / 'dsir.json'
if genux.exists():
    examples.append(('genux-vocab', [sys.executable, str(root / 'scripts' / 'check_vocab_aliases.py'), str(genux)]))
    examples.append(('genux-compile', [sys.executable, str(root / 'scripts' / 'validate_genux_compile_projection.py'), str(genux)]))

for name, cmd in examples:
    subprocess.run(cmd, check=True)
    print(f'REGRESSION_OK {name}')
