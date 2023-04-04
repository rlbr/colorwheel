from pathlib import Path
image_root = Path('/home/raphael/Documents/school/2D/no_backup/Camera/pick/')
tiers = [image_root / f'tier{i}' for i in range(1,5)]
image_paths = [list(tier.glob("*.jpg")) for tier in tiers]
