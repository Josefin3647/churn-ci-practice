import sys

import pandas as pd
import pandera.pandas as pa

SCHEMA = pa.DataFrameSchema(
    {
        "kund_id": pa.Column(int, unique=True),
        "alder": pa.Column(int, pa.Check.in_range(18, 110)),
        "region": pa.Column(str, pa.Check.isin(["Stockholm", "Väst", "Mitt", "Syd", "Norr"])),
        "abonnemang": pa.Column(str, pa.Check.isin(["Bas", "Standard", "Premium"])),
        "manader_som_kund": pa.Column(int, pa.Check.ge(0)),
        "manadskostnad": pa.Column(float, pa.Check.gt(0)),
        "data_gb_per_manad": pa.Column(float, pa.Check.ge(0)),
        "supportarenden_12m": pa.Column(int, pa.Check.ge(0)),
        "avslutat": pa.Column(int, pa.Check.isin([0, 1]))
    },
    strict=True,
)

def main(fil: str) -> int:
    df = pd.read_csv(fil)
    try:
        SCHEMA.validate(df, lazy=True)
    except pa.errors.SchemaErrors as e:
        print(f"STOPP: {fil} har inte rätt format\n")
        print(e.failure_cases[["column", "check"]].value_counts().to_string())
        return 1
    print(f"OK: {fil} ({len(df)} rader)")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))