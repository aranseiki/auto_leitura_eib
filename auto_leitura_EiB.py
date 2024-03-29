# -*- coding: utf8 -*-

from time import sleep
from py_rpautom import web_utils as webutils
from py_rpautom.python_utils import cls
import os

##### Área de configuração #####
senha_curso_eib = os.getenv('senha_curso_eib')
email_curso_eib = os.getenv('email_curso_eib')
numero_modulo = 2
numero_menu_inicial = 7
numero_menu_final = 7
numero_item_extra = 1
url = "https://curso.englishinbrazil.com.br/"
lista_abas_conteudo = [
    'VOCABULARY',
    'GRAMMAR',
    'USEFUL PHRASES',
    'CULTURAL NOTE',
]

webutils.iniciar_navegador(
    nome_navegador="edge",
    options=(
        "--dark",
        "--start-maximized",
        "log-level=3",
        "disable-gpu"
    ),
    url=url,
)

try:
    campo_email = "//input[@placeholder='Email']"
    campo_senha = "//input[@placeholder='Senha']"
    botao_entrar = "//button[@type='submit']"

    validacao_campo_email = ''
    while validacao_campo_email == '':
        webutils.escrever_em_elemento(
            seletor=campo_email,
            texto=email_curso_eib,
            tipo_elemento="xpath",
        )
        sleep(1)
        validacao_campo_email = webutils.coletar_atributo(
            campo_email,
            'value',
            tipo_elemento='xpath',
        )

    webutils.escrever_em_elemento(
        campo_senha,
        texto=senha_curso_eib,
        tipo_elemento="xpath",
    )
    webutils.aguardar_elemento(
        identificador=botao_entrar,
        tipo_elemento="xpath",
    )
    webutils.clicar_elemento(
        botao_entrar,
        tipo_elemento="xpath",
    )

    caminho_modulo = f"(//div[@class='moduloCurso'])[{str(numero_modulo)}]"
    validacao_modulo = False
    while validacao_modulo is False:
        validacao_modulo = webutils.aguardar_elemento(
            identificador=caminho_modulo,
            tipo_elemento="xpath",
        )
    webutils.clicar_elemento(
        caminho_modulo,
        tipo_elemento="xpath",
    )

    menu_hamburguer = "(//div[@class='ant-col'])[1]"
    validacao_menu_hamburguer = False
    while validacao_menu_hamburguer is False:
        validacao_menu_hamburguer = webutils.aguardar_elemento(
            identificador=menu_hamburguer,
            tipo_elemento="xpath",
        )

    for item in range(numero_menu_inicial, numero_menu_final + 1):
        try:
            if item == 8:
                numero_item_extra = 2
            elif item == 15:
                numero_item_extra = 3

            cls()
            print("Estamos exibindo o ítem {} do menu".format(item))

            webutils.aguardar_elemento(
                identificador=menu_hamburguer,
                tipo_elemento="xpath",
            )
            webutils.clicar_elemento(
                menu_hamburguer,
                tipo_elemento="xpath",
            )

            numero_item_menu = item
            caminho_menu = (
                f"(//h2[@class='itemTextoMenuGrupo'])\
                [{str(numero_item_menu + numero_item_extra)}]"
            )
            caminho_infobox = "/parent::div/div/a[3]/div/span[text()='INFOBOX']"

            validacao_caminho_menu = False
            while validacao_caminho_menu is False:
                validacao_caminho_menu = webutils.aguardar_elemento(
                    identificador=caminho_menu,
                    tipo_elemento="xpath",
                )
            webutils.clicar_elemento(
                caminho_menu,
                tipo_elemento="xpath",
            )

            validacao_caminho_infobox = False
            while validacao_caminho_infobox is False:
                validacao_caminho_infobox = webutils.aguardar_elemento(
                    identificador=f"{caminho_menu}{caminho_infobox}",
                    tipo_elemento="xpath"
                )
            webutils.clicar_elemento(
                f"{caminho_menu}{caminho_infobox}",
                tipo_elemento="xpath"
            )

            for aba_conteudo in lista_abas_conteudo:
                print('\n', 'Conteúdo sendo lido agora:', aba_conteudo)
                webutils.aguardar_elemento(
                    identificador=f'//span[text()="{aba_conteudo}"]/parent::button',
                    tipo_elemento="xpath"
                )
                webutils.clicar_elemento(
                    seletor=f'//span[text()="{aba_conteudo}"]/parent::button',
                    tipo_elemento="xpath"
                )

                if aba_conteudo.upper() == 'VOCABULARY':
                    numero_tabela_atual = '1'
                elif aba_conteudo.upper() == 'GRAMMAR':
                    # breakpoint()
                    continue
                elif aba_conteudo.upper() == 'USEFUL PHRASES':
                    numero_tabela_atual = '2'
                elif aba_conteudo.upper() == 'CULTURAL NOTE':
                    numero_tabela_atual = '3'

                linha = 1
                quantidade_linhas = f'(//table)[{numero_tabela_atual}]/tbody/tr'
                resultado_quantidade_linhas = webutils.aguardar_elemento(
                    identificador=quantidade_linhas,
                    tipo_elemento="xpath",
                )
                resultado_quantidade_linhas = webutils.contar_elementos(
                    quantidade_linhas,
                    tipo_elemento="xpath",
                )

                elemento_palavra_padrao = f'((//table)[{numero_tabela_atual}]/tbody/tr/td[2])[#linha]'
                
                elemento_traducao_padrao = f'((//table)[{numero_tabela_atual}]/tbody/tr/td[3])[#linha]'

                botao_play_padrao = f"((//table)[{numero_tabela_atual}]/tbody/tr/td/div/div/div/span/i)[#linha]"

                for linha in range(1, resultado_quantidade_linhas+1):
                    temporizador = 2.5
                    elemento_palavra = elemento_palavra_padrao.replace('#linha', str(linha))
                    elemento_traducao = elemento_traducao_padrao.replace('#linha', str(linha))
                    botao_play = botao_play_padrao.replace('#linha', str(linha))
                    
                    palavra = webutils.extrair_texto(
                        seletor=elemento_palavra,
                        tipo_elemento='xpath',
                    )
                    
                    traducao = webutils.extrair_texto(
                        seletor=elemento_traducao,
                        tipo_elemento='xpath',
                    )

                    tamanho_palavra = len(palavra)
                    if tamanho_palavra > 6:
                        contador_adicional = tamanho_palavra - 6
                        temporizador = temporizador + contador_adicional

                    print(
                        f"linha: {linha} -",
                        f"English: {palavra.strip()} -",
                        f"Português: {traducao.strip()} -",
                        f"Próxima palavra em: {temporizador} segundo(s)."
                    )

                    webutils.clicar_elemento(
                        botao_play,
                        tipo_elemento="xpath",
                    )

                    sleep(temporizador)
        except Exception as errinho:
            print(errinho)
        finally:
            logo_site = "//img[@alt='Logo - English in Brazil']"
            validacao_menu_aberto = webutils.aguardar_elemento(
                identificador=logo_site,
                tipo_elemento='xpath',
                tempo=1,
            )

            if validacao_menu_aberto is True:
                webutils.clicar_elemento(
                    menu_hamburguer, tipo_elemento="xpath"
                )
                while validacao_menu_aberto == True:
                    validacao_menu_aberto = webutils.aguardar_elemento(
                        identificador=logo_site,
                        tipo_elemento='xpath',
                        tempo=0.5,
                    )
except Exception as erro:
    print('Valor de contexto:', erro.__context__)
    print('Número da linha com problema:', erro.__traceback__.tb_lineno)
    print('Mensagem do erro:', erro)
    breakpoint()
finally:
    webutils.encerrar_navegador()
