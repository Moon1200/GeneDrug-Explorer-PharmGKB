# GeneDrug Explorer | مستكشف الجينات والأدوية

Streamlit app to look up the gene variants associated with a drug (or drug class),
their type, level of evidence and phenotype, with an evidence-level chart.

أداة تفاعلية تعرض الطفرات الجينية المرتبطة بدواء أو فئة أدوية، ونوع التأثير ومستوى الأدلة.

## Data | البيانات
`clinicalVariants.tsv` — 5,191 rows, columns: `variant, gene, type, level of evidence, chemicals, phenotypes`.
**Source:** add the dataset source and license here (e.g. PharmGKB clinical variants).

## Notes | ملاحظات
- Drug classes are separated from single drugs by a keyword heuristic (e.g. "agents", "inhibitors"),
  so a few classes may still appear in the drug list.
- This tool **looks up** published associations; it does not predict anything and is not medical advice.

## Run locally | التشغيل
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
Open http://localhost:8501

## Tech | الأدوات
Python · Pandas · Streamlit
