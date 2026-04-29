import subprocess
import time
from pathlib import Path

class OpenFoam:
    def __init__(self, base: str | Path):
        self.base = Path(base).expanduser().resolve()

    def _run(self, case_dir: Path, cmd: list[str]) -> None:
        subprocess.run(cmd, check=True, cwd=case_dir)

    def _simulate_case(self, case_dir: Path) -> None:
        self._run(case_dir, ["blockMesh"])
        self._run(case_dir, ["surfaceFeatures"])
        self._run(case_dir, ["snappyHexMesh", "-overwrite"])
        self._run(case_dir, ["patchSummary"])
        self._run(case_dir, ["potentialFoam"])
        self._run(case_dir, ["simpleFoam"])

    def simulate(self) -> float:
        init = time.time()

        for case_dir in sorted(self.base.iterdir()):
            if case_dir.is_dir():
                self._simulate_case(case_dir)

        end = time.time()
        return end - init
