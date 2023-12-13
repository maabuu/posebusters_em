from pathlib import Path

from energy_minimization import load_molecule, optimize_ligand_in_pocket, prep_ligand, prep_protein
from rdkit.Chem.rdmolfiles import MolFromMolFile

cache_folder = Path("cache")
cache_folder_existed = cache_folder.exists()
cache_folder.mkdir(exist_ok=True)


def test_load_molecule():
    path = Path("test_cases/7MYU_ZR7/7MYU_ZR7_prediction.sdf")

    mol = load_molecule(path)
    assert mol is not None


def test_prep_ligand():
    cache_file = cache_folder / "7MYU_ZR7_ligand_test_prep.sdf"
    ligand_path = Path("test_cases/7MYU_ZR7/7MYU_ZR7_prediction.sdf")

    mol = prep_ligand(ligand_path, temp_file=cache_file)
    assert mol is not None

    mol = prep_ligand(ligand_path, temp_file=cache_file)
    assert mol is not None


def test_prep_protein():
    cache_file = cache_folder / "7MYU_ZR7_protein_test_prep.pdb"
    protein_path = Path("test_cases/7MYU_ZR7/7MYU_ZR7_protein.pdb")

    mol = prep_protein(protein_path, temp_file=cache_file)
    assert mol is not None

    mol = prep_protein(protein_path, temp_file=cache_file)
    assert mol is not None


def test_optimize_ligand_in_pocket():
    protein_file_path = Path("test_cases/7MYU_ZR7/7MYU_ZR7_protein.pdb")
    ligand_file_path = Path("test_cases/7MYU_ZR7/7MYU_ZR7_prediction.sdf")
    output_file_path = Path("./cache/7MYU_ZR7_prediction_minimized.sdf")
    prep_only = False
    name = "7MYU_ZR7"

    opt = optimize_ligand_in_pocket(
        protein_file=protein_file_path,
        ligand_file=ligand_file_path,
        output_file=output_file_path,
        temp_dir=cache_folder,
        prep_only=prep_only,
        name=name,
    )

    # check whether the output ligand exists
    mol_min = opt["ligand"].to_rdkit()
    assert mol_min is not None

    # check whether the output file was written
    mol_min = MolFromMolFile(str(output_file_path), sanitize=True, removeHs=True)
    assert mol_min is not None


if not cache_folder_existed:
    cache_folder.rmdir()
