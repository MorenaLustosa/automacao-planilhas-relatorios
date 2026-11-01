from io import BytesIO
import pandas as pd

REQUIRED=['data','setor','indicador','valor','meta']

def process(df):
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError('Colunas ausentes: '+', '.join(missing))
    data=df.copy()
    data['data']=pd.to_datetime(data['data'],errors='coerce')
    for c in ['valor','meta']: data[c]=pd.to_numeric(data[c],errors='coerce')
    duplicate=data.duplicated(subset=REQUIRED,keep='first')
    missing_values=data[REQUIRED].isna().any(axis=1)
    issues=[]
    for i in range(len(data)):
        reasons=[]
        if duplicate.iloc[i]: reasons.append('duplicata exata')
        if missing_values.iloc[i]: reasons.append('dados ausentes/inválidos')
        if reasons: issues.append({'linha_csv':i+2,'problema':'; '.join(reasons)})
    clean=data[~(duplicate | missing_values)].copy()
    clean['atingiu_meta']=clean['valor']>=clean['meta']
    report=(clean.groupby(['setor','indicador'],as_index=False)
      .agg(registros=('valor','size'),media=('valor','mean'),meta_media=('meta','mean'),percentual_metas_atingidas=('atingiu_meta','mean')))
    return clean,pd.DataFrame(issues,columns=['linha_csv','problema']),report

def to_excel(clean,issues,report):
    output=BytesIO()
    with pd.ExcelWriter(output,engine='openpyxl') as writer:
        clean.to_excel(writer,index=False,sheet_name='Dados tratados')
        issues.to_excel(writer,index=False,sheet_name='Inconsistencias')
        report.to_excel(writer,index=False,sheet_name='Resumo')
    return output.getvalue()
