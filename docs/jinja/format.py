import subprocess
from pathlib import Path


def format_html(text: str, width: int = 80, source_file: str | None = None) -> str:
    command = [
        'npx', '--no', '--',
        'prettier',
        '--experimental-operator-position', 'start',
        '--parser', 'html',
        '--print-width', str(width),
        '--single-quote',
        '--tab-width', '2',
        '--bracket-same-line',
    ]
    if source_file:
        command.extend(['--stdin-filepath', source_file])
    process = subprocess.run(  # nosec
        command, capture_output=True, text=True, check=False, cwd=Path(__file__).parents[1],
        input=text,
    )
    if process.returncode:
        raise RuntimeError(process.stderr or process.stdout)
    return process.stdout.strip()
