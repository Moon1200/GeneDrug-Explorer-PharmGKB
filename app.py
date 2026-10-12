"""GeneDrug Explorer - look up gene variants linked to a drug or drug class.

Data: clinicalVariants.tsv (columns: variant, gene, type, level of evidence,
chemicals, phenotypes) placed next to this file.

Run:  python -m streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent / "clinicalVariants.tsv"

# Heuristic: names containing these words are drug CLASSES, not single drugs.
CATEGORY_KEYWORDS = ["agents", "inhibitors", "blockers", "antagonists",
                     "antivirals", "preparations", "combination", "derivatives",
                     "antibiotics", "diuretics"]

st.set_page_config(page_title="GeneDrug Explorer", layout="wide")
st.markdown("<style>.block-container{direction:rtl;text-align:right}</style>",
            unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE, sep="\t")


def is_drug_class(name: str) -> bool:
    return any(kw in name.lower() for kw in CATEGORY_KEYWORDS)


def split_chemicals(cell) -> list[str]:
    """'a, b' -> ['a', 'b'] (empty list for missing values)."""
    if pd.isna(cell):
        return []
    return [d.strip() for d in str(cell).split(",") if d.strip()]


def get_unique_lists(df: pd.DataFrame):
    """Unique drugs and drug classes (case-insensitive de-duplication)."""
    seen = {}
    for cell in df["chemicals"]:
        for name in split_chemicals(cell):
            seen.setdefault(name.lower(), name)   # keep first spelling
    names = sorted(seen.values(), key=str.lower)
    drugs = [n for n in names if not is_drug_class(n) and n != "3"]
    classes = [n for n in names if is_drug_class(n)]
    return drugs, classes


def get_drug_info(drug_name: str, df: pd.DataFrame) -> pd.DataFrame:
    target = drug_name.lower()
    mask = df["chemicals"].apply(
        lambda x: target in [d.lower() for d in split_chemicals(x)])
    result = df[mask].copy()
    result["phenotypes"] = result["phenotypes"].fillna("غير محدد")
    return result[["gene", "variant", "type", "level of evidence", "phenotypes"]]


# ---------------------------------------------------------------- the UI
st.title("🧬 GeneDrug Explorer")
st.write("اختر دواء أو فئة أدوية لعرض الطفرات الجينية المرتبطة به ومستوى الأدلة.")

if not DATA_FILE.exists():
    st.error("ملف البيانات clinicalVariants.tsv غير موجود بجانب app.py")
    st.stop()

df = load_data()
drugs_unique, drug_classes = get_unique_lists(df)

option_type = st.radio("ابحث حسب:", ["دواء محدد", "فئة أدوية"], horizontal=True)
if option_type == "دواء محدد":
    selected = st.selectbox("اختر الدواء:", drugs_unique)
else:
    selected = st.selectbox("اختر فئة الأدوية:", drug_classes)

if selected:
    result = get_drug_info(selected, df)
    if result.empty:
        st.warning("لا توجد بيانات مرتبطة بهذا الاختيار.")
    else:
        st.subheader(f"النتائج لـ: {selected}")
        st.dataframe(result)

        st.subheader("توزيع مستوى الأدلة")
        st.bar_chart(result["level of evidence"].value_counts())
        st.caption(f"عدد النتائج: {len(result)}")
