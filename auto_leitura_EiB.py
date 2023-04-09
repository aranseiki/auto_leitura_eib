# -*- coding: utf8 -*-

from time import sleep
from py_rpautom import web_utils as webutils
import os


def cls():
    import os
    os.system("cls")


os.environ["WDM_SSL_VERIFY"] = "0"
senha_usuario = os.getenv('senha_curso_eib')


url = "https://curso.englishinbrazil.com.br/"


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
    email = "techall@hotmail.com.br"

    try:
        validacao_campo_email = ''
        while validacao_campo_email == '':
            webutils.escrever_em_elemento(
                seletor=campo_email, texto=email, tipo_elemento="xpath"
            )
            sleep(1)
            validacao_campo_email = webutils.coletar_atributo(
                campo_email,
                'value',
                tipo_elemento='xpath',
            )

        webutils.escrever_em_elemento(
            campo_senha, texto=senha_usuario, tipo_elemento="xpath"
        )
        webutils.aguardar_elemento(
            identificador=botao_entrar, tipo_elemento="xpath"
        )
        webutils.clicar_elemento(botao_entrar, tipo_elemento="xpath")
    except Exception as erro:
        print(erro)
        breakpoint()

    caminho_modulo = "(//div[@class='moduloCurso'])[1]"
    validacao_modulo = False
    while validacao_modulo is False:
        validacao_modulo = webutils.aguardar_elemento(
            identificador=caminho_modulo, tipo_elemento="xpath"
        )
    webutils.clicar_elemento(caminho_modulo, tipo_elemento="xpath")

    menu_hamburguer = "(//div[@class='ant-col'])[1]"
    validacao_menu_hamburguer = False
    while validacao_menu_hamburguer is False:
        validacao_menu_hamburguer = webutils.aguardar_elemento(
            identificador=menu_hamburguer, tipo_elemento="xpath"
        )

    numero_menu_inicial = 5
    numero_menu_final = 5
    numero_item_extra = 1
    for item in range(numero_menu_inicial, numero_menu_final + 1):
        try:
            if item == 8:
                numero_item_extra = 2
            elif item == 15:
                numero_item_extra = 3

            cls()
            print("Estamos exibindo o �tem {} do menu".format(item))

            webutils.clicar_elemento(menu_hamburguer, tipo_elemento="xpath")

            numero_item_menu = item
            caminho_menu = (
                f"(//h2[@class='itemTextoMenuGrupo'])\
                [{str(numero_item_menu + numero_item_extra)}]"
            )
            caminho_infobox = "/parent::div/div/a[3]/div/span[text()='INFOBOX']"

            validacao_caminho_menu = False
            while validacao_caminho_menu is False:
                validacao_caminho_menu = webutils.aguardar_elemento(
                    identificador=caminho_menu, tipo_elemento="xpath"
                )
            webutils.clicar_elemento(caminho_menu, tipo_elemento="xpath")

            validacao_caminho_infobox = False
            while validacao_caminho_infobox is False:
                validacao_caminho_infobox = webutils.aguardar_elemento(
                    identificador=f"{caminho_menu}{caminho_infobox}",
                    tipo_elemento="xpath"
                )
            webutils.clicar_elemento(
                f"{caminho_menu}{caminho_infobox}", tipo_elemento="xpath"
            )

            linha = 1
            quantidade_linhas = "//tbody/tr"
            resultado_quantidade_linhas = webutils.aguardar_elemento(
                identificador=quantidade_linhas, tipo_elemento="xpath"
            )
            resultado_quantidade_linhas = webutils.contar_elementos(
                quantidade_linhas, tipo_elemento="xpath"
            )

            for linha in range(1, resultado_quantidade_linhas+1):
                temporizador = 2.5

                elemento_palavra = f"(//tbody/tr/td[2])[{str(linha)}]"
                palavra = webutils.extrair_texto(
                    seletor=elemento_palavra, tipo_elemento='xpath'
                )

                elemento_traducao = f"(//tbody/tr/td[3])[{str(linha)}]"
                traducao = webutils.extrair_texto(
                    seletor=elemento_traducao, tipo_elemento='xpath'
                )

                print(
                    f"linha: {linha} - English: {palavra} - Portugu�s: {traducao}")

                tamanho_palavra = len(palavra)
                if tamanho_palavra > 6:
                    contador_adicional = tamanho_palavra - 6
                    temporizador = temporizador + contador_adicional

                botao_play = f"(//tbody/tr/td/div/div/div/span/i)[{str(linha)}]"
                webutils.clicar_elemento(botao_play, tipo_elemento="xpath")

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
    breakpoint()
finally:
    webutils.encerrar_navegador()
