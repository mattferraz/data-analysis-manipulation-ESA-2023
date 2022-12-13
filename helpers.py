import pandas
import pdfkit as pdfkit


# Para cada candidato na lista da ESA, verificar, se existir, a classificação do mesmo na ESPCEX e EFOMM
def include_others_class_to_esa_list(esa_list: pandas.DataFrame,
                                     espcex_listed_names_and_ranks: list[list],
                                     afa_listed_names_and_ranks: list[list],
                                     eear1_listed_names_and_ranks: list[list],
                                     eear2_listed_names_and_ranks: list[list],
                                     en_listed_names_and_ranks: list[list],
                                     efomm_listed_names_and_ranks: list[list],
                                     eam_listed_names_and_ranks: list[list]) -> pandas.DataFrame:
    class_espcex = []
    class_afa = []
    class_eear1 = []
    class_eear2 = []
    class_en = []
    class_efomm = []
    class_eam = []

    for name in esa_list['Nome']:
        class_espcex.append(get_others_rank_by_candidate_name(name, espcex_listed_names_and_ranks))
        class_afa.append(get_others_rank_by_candidate_name(name, afa_listed_names_and_ranks))
        class_eear1.append(get_others_rank_by_candidate_name(name, eear1_listed_names_and_ranks))
        class_eear2.append(get_others_rank_by_candidate_name(name, eear2_listed_names_and_ranks))
        class_en.append(get_others_rank_by_candidate_name(name, en_listed_names_and_ranks))
        class_efomm.append(get_others_rank_by_candidate_name(name, efomm_listed_names_and_ranks))
        class_eam.append(get_others_rank_by_candidate_name(name, eam_listed_names_and_ranks))

    esa_list = esa_list.assign(EsPCEX=class_espcex,
                               AFA=class_afa,
                               EEAR_1=class_eear1,
                               EEAR_2=class_eear2,
                               EN=class_en,
                               EFOMM=class_efomm,
                               EAM=class_eam)

    return esa_list


def get_others_rank_by_candidate_name(name: str,
                                      listed_names_and_ranks: list[list]):
    rank = None
    try:
        idx_class = listed_names_and_ranks[0].index(name)
        rank = int(listed_names_and_ranks[1][idx_class])
    except ValueError:
        rank = ''
    finally:
        return rank


def generate_esa_rank_pdf_from_dataframe(ampla: pandas.DataFrame,
                                         cota: pandas.DataFrame,
                                         gender: str,
                                         pdf_title: str,
                                         info1: str,
                                         output_file_name: str):
    html_main_structure = '''
    <html>
      <head><title>{title}</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <meta charset="UTF-8">
      <body>
        <p class="title">LISTA NÃO OFICIAL</p>
        <p class="info1">{info1}</p>
        <p class="infos">a. A lista de candidatos classificados e majorados a seguir NÃO se trata de uma lista oficial. 
        Esta é uma versão alterada que tem como único e exclusivo objetivo permitir que o candidato analise a sua 
        situação de forma mais ampla e a possibilidade de prosseguimento para as demais etapas do concurso.</p>
        <p class="infos">b. Apesar de não estarem presentes nas classificações, as especialidades de cada concurso foram 
        levadas em consideração. Então um candidato que consta como primeiro colocado em outro concurso na lista abaixo, 
        pode ser de qualquer uma das diferentes especialidades da instituição em análise.</p>
        <p class="label">Feito por Mateus: https://t.me/lk_mzt</p>
        <p>
            1. ÁREA GERAL, CANDIDATOS CLASSIFICADOS E MAJORADOS, SEXO {gender}, AMPLA CONCORRÊNCIA
        </p>
        {ampla_table}<br/>
        <p>
            2. ÁREA GERAL, CANDIDATOS CLASSIFICADOS E MAJORADOS, SEXO {gender}, VAGAS RESERVADAS (Lei 12.990/14)
        </p>
        {cota_table}
      </body>
    </html>
    '''

    with open(f"{output_file_name}.html", "w", encoding="utf-8") as file:
        file.write(html_main_structure.format(title=pdf_title,
                                              info1=info1,
                                              gender=gender.upper(),
                                              ampla_table=ampla.to_html(index=False),
                                              cota_table=cota.to_html(index=False)))
    options = {
        "enable-local-file-access": None,
        'encoding': "UTF-8"
    }
    pdfkit.from_file(input=f'{output_file_name}.html', css='df_style.css', output_path=f'{output_file_name}.pdf',
                     options=options)
