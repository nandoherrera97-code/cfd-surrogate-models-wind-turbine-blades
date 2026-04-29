import subprocess
import time
from pathlib import Path
from typing import Union, List
import shutil

class OpenFoam:
    def __init__(self, base: Union[str, Path]):
        self.base = Path(base)

    def _run(self, case_dir: Path, cmd: List[str]) -> None:
        subprocess.run(cmd, check=True, cwd=case_dir)

    def _simulate_case(self, case_dir: Path) -> None:
        self._run(case_dir, ["blockMesh"])
        self._run(case_dir, ["surfaceFeatures"])
        self._run(case_dir, ["snappyHexMesh", "-overwrite"])
        self._run(case_dir, ["patchSummary"])
        self._run(case_dir, ["potentialFoam"])
        self._run(case_dir, ["simpleFoam"])

    def simulate(self, batch_size: int = 10) -> float:
        init = time.time()

        results_dir = self.base / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        while True:
            # Lista de casos pendientes (excluye la carpeta results)
            pending = sorted(
                p for p in self.base.iterdir()
                if p.is_dir() and p.name != results_dir.name
            )

            if not pending:
                break

            batch = pending[:batch_size]

            for case_dir in batch:
                # si esto falla, se detendrá aquí (por check=True)
                self._simulate_case(case_dir)

                # mueve el caso terminado a results/
                dst = results_dir / case_dir.name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(case_dir), str(dst))

        return time.time() - init


if __name__ == "__main__":
    base = r"D:/Programa/blueCFD-Core-2020/ofuser-of8/run"
    runner = OpenFoam(base)
    elapsed = runner.simulate(batch_size=10)
    print(f"Total execution time: {elapsed:.2f} s")
