import pandas as pd
import tabula
from PyPDF2 import PdfMerger

import helpers

TEXT1_FEM = 'LISTA DE CANDIDATAS CLASSIFICADAS DENTRO DO NÚMERO DE VAGAS E CLASSIFICADAS MAJORADAS CONSIDERANDO O ' \
            'RESULTADO FINAL DO EXAME INTELECTUAL DA ÁREA GERAL, SEGMENTO FEMININO, DO CONCURSO DE ADMISSÃO AOS ' \
            'CURSOS DE FORMAÇÃO E GRADUAÇÃO DE SARGENTOS 2023/24 '

TEXT1_MASC = 'LISTA DE CANDIDATOS CLASSIFICADOS DENTRO DO NÚMERO DE VAGAS E CLASSIFICADOS MAJORADOS CONSIDERANDO O ' \
             'RESULTADO FINAL DO EXAME INTELECTUAL DA ÁREA GERAL, SEGMENTO MASCULINO, DO CONCURSO DE ADMISSÃO AOS ' \
             'CURSOS DE FORMAÇÃO E GRADUAÇÃO DE SARGENTOS 2023/24 '

if __name__ == '__main__':
    # Classificados EsPCEx:
    pdf_path = 'pdfs/exercito/espcex/classificados-EsPCEx.pdf'
    espcex_class_df = pd.concat(tabula.read_pdf(pdf_path, pages='2-12', lattice=True)).replace('\r', ' ', regex=True)

    # Majorados EsPCEX:
    pdf_path = 'pdfs/exercito/espcex/majorados-EsPCEX.pdf'
    espcex_maj_df = pd.concat(tabula.read_pdf(pdf_path, pages='2-9', lattice=True)).replace('\r', ' ', regex=True)

    # Classificados e Majorados EN:
    pdf_path = 'pdfs/marinha/en/convocados-en-2023.pdf'
    en_df = pd.concat(tabula.read_pdf(pdf_path, pages='all', lattice=True, pandas_options={'header': None}),
                      ignore_index=True)[[1, 6]].replace('\r', ' ', regex=True).drop([0, 95])
    en_df = pd.concat([
        en_df.iloc[0:94].sort_values(6, ascending=False).reset_index(drop=True).assign(Class=lambda x: x.index + 1),
        en_df.iloc[94:].sort_values(6, ascending=False).reset_index(drop=True).assign(Class=lambda x: x.index + 1)
    ], ignore_index=True)

    # Classificados e Majorados EFOMM — CIAGA:
    pdf_path = 'pdfs/marinha/efomm/classificados-EFOMM-ciaga.pdf'
    efomm_ciaga_df = pd.concat(tabula.read_pdf(pdf_path, pages='all', lattice=True, pandas_options={'header': None}),
                               ignore_index=True).replace('\r', ' ', regex=True).drop([0, 87]).reset_index(drop=True)

    # Classificados e Majorados EFOMM — CIABA:
    pdf_path = 'pdfs/marinha/efomm/classificados-EFOMM-ciaba.pdf'
    efomm_ciaba_df = pd.concat(tabula.read_pdf(pdf_path, pages='all', lattice=True, pandas_options={'header': None}),
                               ignore_index=True).replace('\r', ' ', regex=True).drop([0, 92]).reset_index(drop=True)

    # Classificados e Majorados EAM:
    pdf_path = 'pdfs/marinha/eam/convocados-eam-2023.pdf'
    eam_df = pd.concat(tabula.read_pdf(pdf_path, pages='all', lattice=True, pandas_options={'header': None}),
                       ignore_index=True)[[1, 7]].replace('\r', ' ', regex=True).drop([0, 1, 98])
    eam_df = pd.concat([
        eam_df.iloc[0:96].sort_values(7, ascending=False).reset_index(drop=True).assign(Class=lambda x: x.index + 1),
        eam_df.iloc[96:].sort_values(7, ascending=False).reset_index(drop=True).assign(Class=lambda x: x.index + 1)
    ], ignore_index=True)

    # Classificados e Majorados AFA:
    pdf_path = 'pdfs/aeronautica/afa/convocados-afa-2023.pdf'
    afa_df = pd.concat(map(lambda x: x.dropna(axis='columns'), tabula.read_pdf(pdf_path, pages='1-30', stream=True)),
                       ignore_index=True)[['Nome', 'Class']].replace('\r', ' ', regex=True)

    # Classificados e Majorados EEAR 2023.1:
    merger = PdfMerger()
    source_path = './pdfs/aeronautica/eear/2023.1'
    pdfs = [
        f'{source_path}/primeira-convocacao/bct.pdf', f'{source_path}/segunda-convocacao/bct.pdf',
        f'{source_path}/primeira-convocacao/opc01.pdf', f'{source_path}/segunda-convocacao/opc01.pdf',
        f'{source_path}/primeira-convocacao/opc02.pdf', f'{source_path}/segunda-convocacao/opc02.pdf',
        f'{source_path}/primeira-convocacao/opc03.pdf', f'{source_path}/segunda-convocacao/opc03.pdf'
    ]

    for pdf in pdfs:
        merger.append(pdf)
    merger.write(f'{source_path}/eear-convocacao-2023.1.pdf')
    merger.close()

    pdf_path = 'pdfs/aeronautica/eear/2023.1/eear-convocacao-2023.1.pdf'
    eear1_df = pd.concat(tabula.read_pdf(pdf_path, pages='all', lattice=True),
                         ignore_index=True).iloc[:, [0, 4]].replace('\r', ' ', regex=True)
    eear1_df.columns = ['Nome', 'Class']

    # Classificados e Majorados EEAR 2023.2:
    pdf_path = 'pdfs/aeronautica/eear/2023.2/resultado-provisorio/bct.pdf'
    eear2_bct_df = tabula.read_pdf(pdf_path, pages='181-193', lattice=True, pandas_options={'header': None})
    eear2_bct_df = pd.concat([eear2_bct_df[index] for index in range(0, len(eear2_bct_df)) if (index + 1) % 3 == 0],
                             ignore_index=True)[[0, 4]].iloc[-410:].replace('\r', ' ', regex=True).reset_index(drop=True)

    pdf_path = 'pdfs/aeronautica/eear/2023.2/resultado-provisorio/opc01.pdf'
    eear2_opc01_df = tabula.read_pdf(pdf_path, pages='87-90', lattice=True, pandas_options={'header': None})
    eear2_opc01_df = pd.concat([eear2_opc01_df[index] for index in range(0, len(eear2_opc01_df)) if (index + 1) % 3 == 0],
                               ignore_index=True)[[0, 4]].iloc[-95:].replace('\r', ' ', regex=True).reset_index(drop=True)

    pdf_path = 'pdfs/aeronautica/eear/2023.2/resultado-provisorio/opc02.pdf'
    eear2_opc02_df = tabula.read_pdf(pdf_path, pages='304-321', lattice=True, pandas_options={'header': None})
    eear2_opc02_df = pd.concat([eear2_opc02_df[index] for index in range(0, len(eear2_opc02_df)) if (index + 1) % 3 == 0],
                               ignore_index=True)[[0, 4]].iloc[-573:].replace('\r', ' ', regex=True).reset_index(drop=True)

    eear2_df = pd.concat([eear2_bct_df, eear2_opc01_df, eear2_opc02_df], ignore_index=True)
    eear2_df.columns = ['Nome', 'Class']

    # Classificados e Majorados ESA — Masculino:
    pdf_path = 'pdfs/exercito/esa/classificados-ESA-masc.pdf'
    dfs_esa_ampla_masc = tabula.read_pdf(pdf_path, pages='all', lattice=True)
    for df in dfs_esa_ampla_masc:
        df.dropna(axis='columns', inplace=True)
        df.drop(df.columns[1], axis='columns', inplace=True)
        df.columns = ['Classificação', 'Nome', 'OMSE', 'Cotista', 'Nota']
    esa_ampla_masc_list = pd.concat(dfs_esa_ampla_masc[0:74], ignore_index=True).replace('\r', ' ', regex=True)
    esa_cota_masc_list = pd.concat(dfs_esa_ampla_masc[74:], ignore_index=True).replace('\r', ' ', regex=True)

    # Classificados e Majorados ESA — Feminino:
    pdf_path = 'pdfs/exercito/esa/classificados-ESA-fem.pdf'
    dfs_esa_fem = tabula.read_pdf(pdf_path, pages='all', lattice=True, pandas_options={'header': None})
    for index in range(len(dfs_esa_fem)):
        dfs_esa_fem[index].dropna(axis='columns', inplace=True)
        dfs_esa_fem[index].drop(dfs_esa_fem[index].columns[1], axis='columns', inplace=True)
        if index not in [1, 2, 12]:
            dfs_esa_fem[index].drop(0, inplace=True)
        dfs_esa_fem[index].columns = ['Classificação', 'Nome', 'OMSE', 'Cotista', 'Nota']
    final_esa_ampla_fem = pd.concat(dfs_esa_fem[0:11], ignore_index=True).replace('\r', ' ', regex=True)
    final_esa_cota_fem = pd.concat(dfs_esa_fem[11:], ignore_index=True).replace('\r', ' ', regex=True)

    espcex_listed_names_and_ranks = [
        pd.concat([espcex_class_df['Nome'], espcex_maj_df['Nome']]).tolist(),
        pd.concat([espcex_class_df['Class'], espcex_maj_df['Class']]).tolist()
    ]

    afa_listed_names_and_ranks = [afa_df['Nome'].tolist(), afa_df['Class'].tolist()]

    eear1_listed_names_and_ranks = [eear1_df['Nome'].tolist(), eear1_df['Class'].tolist()]

    eear2_listed_names_and_ranks = [eear2_df['Nome'].tolist(), eear2_df['Class'].tolist()]

    en_listed_names_and_ranks = [en_df[1].tolist(), en_df['Class'].tolist()]

    eam_listed_names_and_ranks = [eam_df[1].tolist(), eam_df['Class'].tolist()]

    efomm_listed_names_and_ranks = [
        pd.concat([efomm_ciaga_df[1], efomm_ciaba_df[1]]).tolist(),
        pd.concat([efomm_ciaga_df[0], efomm_ciaba_df[0]]).tolist()
    ]

    final_esa_ampla_masc = helpers.include_others_class_to_esa_list(esa_ampla_masc_list,
                                                                    espcex_listed_names_and_ranks,
                                                                    afa_listed_names_and_ranks,
                                                                    eear1_listed_names_and_ranks,
                                                                    eear2_listed_names_and_ranks,
                                                                    en_listed_names_and_ranks,
                                                                    efomm_listed_names_and_ranks,
                                                                    eam_listed_names_and_ranks)

    esa_cota_masc_list = helpers.include_others_class_to_esa_list(esa_cota_masc_list,
                                                                  espcex_listed_names_and_ranks,
                                                                  afa_listed_names_and_ranks,
                                                                  eear1_listed_names_and_ranks,
                                                                  eear2_listed_names_and_ranks,
                                                                  en_listed_names_and_ranks,
                                                                  efomm_listed_names_and_ranks,
                                                                  eam_listed_names_and_ranks)

    final_esa_ampla_fem = helpers.include_others_class_to_esa_list(final_esa_ampla_fem,
                                                                   espcex_listed_names_and_ranks,
                                                                   afa_listed_names_and_ranks,
                                                                   eear1_listed_names_and_ranks,
                                                                   eear2_listed_names_and_ranks,
                                                                   en_listed_names_and_ranks,
                                                                   efomm_listed_names_and_ranks,
                                                                   eam_listed_names_and_ranks)

    final_esa_cota_fem = helpers.include_others_class_to_esa_list(final_esa_cota_fem,
                                                                  espcex_listed_names_and_ranks,
                                                                  afa_listed_names_and_ranks,
                                                                  eear1_listed_names_and_ranks,
                                                                  eear2_listed_names_and_ranks,
                                                                  en_listed_names_and_ranks,
                                                                  efomm_listed_names_and_ranks,
                                                                  eam_listed_names_and_ranks)

    helpers.generate_esa_rank_pdf_from_dataframe(ampla=final_esa_ampla_masc,
                                                 cota=esa_cota_masc_list,
                                                 gender='Masculino',
                                                 pdf_title='Classificados e Majorados Masculino ESA 2023',
                                                 info1=TEXT1_MASC,
                                                 output_file_name='resultado_esa_masculino')

    helpers.generate_esa_rank_pdf_from_dataframe(ampla=final_esa_ampla_fem,
                                                 cota=final_esa_cota_fem,
                                                 gender='Feminino',
                                                 pdf_title='Classificadas e Majoradas Feminino ESA 2023',
                                                 info1=TEXT1_FEM,
                                                 output_file_name='resultado_esa_feminino')
